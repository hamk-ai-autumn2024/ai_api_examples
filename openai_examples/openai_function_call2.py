from openai import OpenAI
import json
import requests
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
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text content, removing scripts and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return None

# Create a running input list we will add to over time
input_list = [
    {"role": "user", "content": "Can you fetch the content from https://platform.openai.com/docs/guides/function-calling and summarize it for me?"}
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

print("Final input:")
print(input_list)

response = client.responses.create(
    model="gpt-5",
    instructions="Summarize the content fetched from the URL in a clear and concise manner.",
    tools=tools,
    input=input_list,
)

# 5. The model should be able to give a response!
print("Final output:")
print(response.model_dump_json(indent=2))
print("\n" + response.output_text)