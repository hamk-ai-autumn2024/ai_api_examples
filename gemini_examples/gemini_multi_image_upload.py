from google import genai
from google.genai import types
import PIL.Image
import os

print("Uploading files...")

image1 = PIL.Image.open("gomoto.jpg")
image2 = PIL.Image.open("gomoto3.jpg")
image3 = PIL.Image.open("gomoto3.jpg")

print(f"Uploaded files: {image1.filename}, {image2.filename}, {image3.filename}")
print("Generating...")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["Invent advertising slogans for the following images", image1, image2, image3],
)
print(response.text)


