from google import genai
import os

# This assuemes that you have set the environment variable GEMINI_API_KEY with your API key.
client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

myfile = client.files.upload(file='speech.mp3')
prompt = 'Generate a transcript of the speech.'

response = client.models.generate_content(
  model='gemini-2.5-flash',
  contents=[prompt, myfile]
)

print(response.text)