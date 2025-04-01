import base64
import requests
import os
import sys
from openai import OpenAI
from file_util import fetch_url, save_binary_file, find_new_file_name

# OpenAI API Key
# api_key = "YOUR_OPENAI_API_KEY"  # unsafe way
api_key = os.getenv(
    "OPENAI_API_KEY"
)  # set your OPENAI_API_KEY in an environment variable

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Path to your image
image_path = "dall_0.png"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What’s in this image?"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
    "max_tokens": 100,
}
print("Sending request to OpenAI Vision API...")
response = requests.post(
    "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
)

#print(response.json())
text_description = response.json().get("choices")[0].get("message").get("content")
print(text_description)

client = OpenAI()  # use the API key from the OPENAI_API_KEY environment variable
print("Generating image...")
response = client.images.generate(
  model="dall-e-3",
  prompt=text_description,
  size="1024x1024",  #size="1792x1024", #size="1024x1792",
  quality="hd",  #quality="standard",
  style="vivid",  #style="natural",
  n=1,  # number of images to generate, Dall-E 3 accepts just 1
)

image_url = response.data[0].url
print(image_url)

print("Downloading image...")
# Download the image
image_data = fetch_url(image_url)
# Save the image to a file
if image_data is not None:
    file_name = find_new_file_name("dall.png")
    if save_binary_file(data=image_data, filename=file_name):
      print(f"Image saved to {file_name}")

