import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content("Write a story about a very unlucky man who wins the lottery.")
print(response.text)
