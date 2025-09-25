import os
import requests
from bs4 import BeautifulSoup
import anthropic

# Prefer a stable/latest alias to avoid hard-coding a dated model ID
model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")


def load_url(url: str, timeout: int = 15, max_chars: int = 80_000) -> str | None:
    """Load URL and return plain text content (truncated), or None if loading fails."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        resp = requests.get(url, timeout=timeout, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return text[:max_chars]
    except Exception as e:
        print(f"Error loading URL: {e}")
        return None


def find_tool_uses(content_blocks):
    """Return a list of tool_use blocks from assistant content blocks."""
    return [b for b in content_blocks if getattr(b, "type", None) == "tool_use"]


def extract_all_text(content_blocks):
    """Concatenate text from text-type blocks."""
    parts = []
    for b in content_blocks:
        if getattr(b, "type", None) == "text":
            # For SDKs that wrap text as an object with .text, handle both
            text = getattr(b, "text", None)
            if text is None and isinstance(getattr(b, "content", None), str):
                text = b.content
            if text:
                parts.append(text)
    return "\n\n".join(parts) if parts else ""


def main():
    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Define the tool
    tools = [
        {
            "name": "load_url",
            "description": "Load a URL and return its text content",
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to load"
                    }
                },
                "required": ["url"],
            },
        }
    ]

    # Sample URL
    sample_url = (
        "https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview"
    )

    # Build conversation and strongly require tool use for external content
    system_prompt = (
        "You are a helpful assistant. If the user asks for content from any external URL, "
        "you must call the provided tools to retrieve that content. Do not fabricate summaries."
    )
    history = [
        {
            "role": "user",
            "content": (
                f"Please load the content from {sample_url} and provide a brief summary of what it contains."
            ),
        },
    ]

    # First assistant response
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        tools=tools,
        system=system_prompt,
        messages=history,
    )

    # Keep a loop to handle tool calls (up to a few rounds)
    max_rounds = 3
    rounds = 0
    final_message = message

    while rounds < max_rounds:
        rounds += 1
        tool_calls = find_tool_uses(final_message.content)
        if not tool_calls:
            break

        # Append assistant message with its content blocks
        history.append({"role": "assistant", "content": final_message.content})

        # Execute tool calls and bundle results in a single user message
        tool_results = []
        for call in tool_calls:
            if getattr(call, "name", None) == "load_url":
                url = None
                # Some SDKs provide a dict in .input; guard carefully
                try:
                    url = call.input.get("url") if hasattr(call, "input") else None
                except Exception:
                    url = None
                if not url:
                    url = sample_url  # fallback to requested URL
                content = load_url(url) or "Failed to load URL content"
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": call.id,
                        "content": content,
                    }
                )
            else:
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": call.id,
                        "content": f"Tool '{getattr(call, 'name', 'unknown')}' is not implemented.",
                        "is_error": True,
                    }
                )

        # Send all tool results back
        history.append({"role": "user", "content": tool_results})

        # Ask for the follow-up assistant response (allowing further tool use if needed)
        final_message = client.messages.create(
            model=model,
            max_tokens=1000,
            tools=tools,
            system=system_prompt,
            messages=history,
        )

    # Print the final assistant text
    text = extract_all_text(final_message.content)
    if not text:
        # Fallback: print the first block's text-ish content
        try:
            text = final_message.content[0].text
        except Exception:
            text = str(final_message.content[0]) if final_message.content else "(no content)"
    print("Summary:")
    print(text)

if __name__ == "__main__":
    main()