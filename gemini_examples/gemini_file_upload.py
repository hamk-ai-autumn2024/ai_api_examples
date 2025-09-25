from google import genai
from google.genai import types
import pathlib
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Retrieve and encode the PDF byte
filepath = pathlib.Path('Robinson_Crusoe_BT.pdf')

prompt = "Summarize the story and list the main characters"
response = client.models.generate_content(
  model="gemini-2.5-flash",
  contents=[
      types.Part.from_bytes(
        data=filepath.read_bytes(),
        mime_type='application/pdf',
      ),
      prompt])
print(response.text)