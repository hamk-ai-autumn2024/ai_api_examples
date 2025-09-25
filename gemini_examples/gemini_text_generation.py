from google import genai
import os 

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work? Give a concise answer with few examples and sentences.",
)
print(response.text)
