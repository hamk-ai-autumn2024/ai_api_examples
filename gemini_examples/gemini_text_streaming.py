import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content("Explain black holes in increasing steps of complexity", stream=True)
for chunk in response:
    print(chunk.text, flush=True)
