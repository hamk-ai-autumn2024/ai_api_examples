from google import genai
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"]  )

response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=["Explain black holes in increasing steps of complexity"]
)
for chunk in response:
    print(chunk.text, end="")


