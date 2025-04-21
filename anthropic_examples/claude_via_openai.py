from openai import OpenAI
import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = OpenAI(
    api_key=ANTHROPIC_API_KEY,  # Your Anthropic API key
    base_url="https://api.anthropic.com/v1/"  # Anthropic's API endpoint
)

response = client.chat.completions.create(
    model="claude-3-7-sonnet-20250219", # Anthropic model name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who are you?"}
    ],
)

print(response.choices[0].message.content)