import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel(
    model_name='gemini-1.5-pro',
    tools='code_execution')

# NOTE: The code is executed in a sandboxed environment on Google servers
response = model.generate_content((
    'What are permutations of the word "BACH"?'
    'Generate and run code. Print all the permutations.'))

print(response.text)
