from openai import OpenAI
import json
import requests
import httpx
from bs4 import BeautifulSoup

client = OpenAI()

# 1. Define a list of callable tools for the model
tools = [
    {
        "type": "function",
        "name": "fetch_url",
        "description": "Fetch and extract text content from a given URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to fetch content from",
                },
            },
            "required": ["url"],
        },
    },
]

def fetch_url(url):
    """
    Attempts to fetch given URL and parse the text contents of the HTML file.
    Returns the text contents only. Returns None if it fails.

    Many modern sites block default Python user agents with a 403. We:
    - Send realistic browser headers (Chrome on Windows)
    - Use a requests.Session for cookies/connection reuse
    - Fall back to httpx with HTTP/2 enabled if the first attempt fails or returns 403
    """

    def _extract_text(html_bytes: bytes) -> str:
        soup = BeautifulSoup(html_bytes, 'html.parser')
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        # Normalize whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        cleaned = ' '.join(chunk for chunk in chunks if chunk)
        return cleaned

    # Browser-like headers
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://platform.openai.com/",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        # Some WAFs look at these; optional but harmless:
        "Upgrade-Insecure-Requests": "1",
    }

    # First attempt: requests (HTTP/1.1)
    try:
        with requests.Session() as s:
            s.headers.update(headers)
            resp = s.get(url, timeout=15)
            if resp.status_code == 403:
                raise requests.HTTPError(f"403 Forbidden for url: {url}")
            resp.raise_for_status()
            return _extract_text(resp.content)
    except Exception as e1:
        # Fall back to HTTP/2 client (some CDNs/WAFs prefer it)
        try:
            with httpx.Client(http2=True, headers=headers, timeout=15, follow_redirects=True) as client:
                resp2 = client.get(url)
                if resp2.status_code == 403:
                    raise httpx.HTTPStatusError("403 Forbidden", request=resp2.request, response=resp2)
                resp2.raise_for_status()
                return _extract_text(resp2.content)
        except Exception as e2:
            print(f"Error fetching URL {url}: {e2}")
            return None

# Create a running input list we will add to over time
input_list = [
    {"role": "user", "content": "Can you fetch the content from https://openai.com/index/introducing-upgrades-to-codex/ and summarize it for me?"}
]

# 2. Prompt the model with tools defined
response = client.responses.create(
    model="gpt-5",
    tools=tools,
    input=input_list,
)

# Save function call outputs for subsequent requests
input_list += response.output

for item in response.output:
    if item.type == "function_call":
        if item.name == "fetch_url":
            # 3. Execute the function logic for fetch_url
            arguments = json.loads(item.arguments)
            url_content = fetch_url(arguments["url"])
            
            # 4. Provide function call results to the model
            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps({
                  "content": url_content
                })
            })

response = client.responses.create(
    model="gpt-5",
    instructions="Summarize the content fetched from the URL in a clear and concise manner.",
    tools=tools,
    input=input_list,
)

# 5. The model should be able to give a response!
print(response.output_text)