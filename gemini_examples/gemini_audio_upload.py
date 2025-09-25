from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
print("Uploading file...")

myfile = client.files.upload(file='petri_speech_sample.wav')
prompt = 'Generate a transcript of the speech. Then translate into Finnish.' 
print("Analyzing...")

response = client.models.generate_content(
  model='gemini-2.5-flash',
  contents=[prompt, myfile]
)

print(response.text)
