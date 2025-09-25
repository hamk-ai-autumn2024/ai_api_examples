import os
import requests
from bs4 import BeautifulSoup
import anthropic

model = "claude-sonnet-4-20250514"

def load_url(url):
    """Load URL and return text content, or None if loading fails."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text(strip=True)
    except Exception as e:
        print(f"Error loading URL: {e}")
        return None

def main():
    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
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
                "required": ["url"]
            }
        }
    ]
    
    # Sample URL
    sample_url = "https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview"
    
    # Create message with tool use request
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        tools=tools,
        messages=[
            {
                "role": "user",
                "content": f"Please load the content from {sample_url} and provide a brief summary of what it contains."
            }
        ]
    )
    
    # Process the response
    if message.content[0].type == "tool_use":
        tool_use = message.content[0]
        if tool_use.name == "load_url":
            url = tool_use.input["url"]
            content = load_url(url)
            
            # Send the tool result back to Claude
            response = client.messages.create(
                model=model,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": f"Please load the content from {sample_url} and provide a brief summary of what it contains."
                    },
                    {
                        "role": "assistant",
                        "content": message.content
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use.id,
                                "content": content if content else "Failed to load URL content"
                            }
                        ]
                    }
                ]
            )
            
            print("Summary:")
            print(response.content[0].text)
    else:
        print("No tool use requested")
        print(message.content[0].text)

if __name__ == "__main__":
    main()