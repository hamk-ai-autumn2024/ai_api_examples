import google.generativeai as genai
import PIL.Image
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
print("Uploading files...")

image1 = PIL.Image.open("gomoto.jpg")
image2 = PIL.Image.open("gomoto3.jpg")
image3 = PIL.Image.open("gomoto3.jpg")

print(f"Uploaded files: {image1.filename}, {image2.filename}, {image3.filename}")
print("Generating...")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
# Prompt the model with text and the previously uploaded image.
response = model.generate_content(["Invent advertising slogans for the following images", image1, image2, image3])
print(response.text)
