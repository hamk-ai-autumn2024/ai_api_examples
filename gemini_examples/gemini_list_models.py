import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
print("Available models:")
for model in client.models.list():
    print(model.name)
