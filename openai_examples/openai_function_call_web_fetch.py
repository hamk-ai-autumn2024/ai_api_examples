from openai import OpenAI
import json
import socket
import sys
from html.parser import HTMLParser
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

client = OpenAI()

MAX_SUMMARY_WORDS = 100


class _HTMLToTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []
        self._suppress_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self._suppress_depth += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self._suppress_depth > 0:
            self._suppress_depth -= 1

    def handle_data(self, data):
        if self._suppress_depth == 0:
            text = data.strip()
            if text:
                self._parts.append(text)

    def get_text(self):
        return " ".join(self._parts)


def load_url(url: Optional[str]) -> Optional[str]:
    if not url:
        return None

    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=10) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            html = response.read().decode(charset, errors="replace")
    except (HTTPError, URLError, socket.timeout, ValueError):
        return None

    parser = _HTMLToTextParser()
    try:
        parser.feed(html)
        parser.close()
    except Exception:
        return None

    text = parser.get_text()
    return text if text else None


def _limit_words(text: str, max_words: int = MAX_SUMMARY_WORDS) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words])


def main():
    # 1. Define a list of callable tools for the model
    tools = [
        {
            "type": "function",
            "name": "load_url",
            "description": "Retrieve the text content of a web page.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The HTTP or HTTPS URL to load.",
                    },
                },
                "required": ["url"],
            },
        },
    ]

    # Create a running input list we will add to over time
    input_list = [
        {
            "role": "user",
            "content": "Please load https://en.wikipedia.org/wiki/OpenAI and share the text content.",
        }
    ]

    try:
        response = client.responses.create(
            model="gpt-5",
            tools=tools,
            input=input_list,
        )
    except KeyboardInterrupt:
        print("Interrupted before tool call.", file=sys.stderr)
        return

    # Save function call outputs for subsequent requests
    input_list += response.output

    for item in response.output:
        if item.type == "function_call" and item.name == "load_url":
            args = json.loads(item.arguments or "{}")
            url = args.get("url")
            content = load_url(url)

            # 3. Execute the function logic for load_url
            input_list.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({"text": content}),
                }
            )

    print("Tool call complete. Summarizing response...")

    summary_instructions = (
        "Summarize the retrieved URL content in no more than 100 words. "
        "If the URL could not be loaded, explain the issue in fewer than 50 words."
    )

    try:
        response = client.responses.create(
            model="gpt-5-nano",
            instructions=summary_instructions,
            tools=tools,
            input=input_list,
        )
    except KeyboardInterrupt:
        print("Interrupted before summary.", file=sys.stderr)
        return

    summary_text = response.output_text.strip()
    summary = _limit_words(summary_text)

    print("Summary (<= 100 words):")
    print(summary)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Aborted by user.", file=sys.stderr)
