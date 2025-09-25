from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents="How does AI work? Give a concise answer with few examples and sentences.",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=1000) # Disables thinking
    ),
)
print(response.text)