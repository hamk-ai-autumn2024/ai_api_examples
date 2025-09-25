from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
print("Uploading file...")
with open('malta.jpg', 'rb') as f:
   image_bytes = f.read()
   print("Analyzing...")
   response = client.models.generate_content(
      model='gemini-2.5-flash',
      contents=[
         types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/jpeg',
            ),
            'Desribe the image in detail. Read the texts in the image.'
            ]
        )

print(response.text)
