# Using LM Studio's Llava model to describe an image from a local file
# Adapted from OpenAI's Vision example
from openai import OpenAI
import base64
import sys
import requests

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Ask the user for a path on the filesystem:
path = input("Enter a local filepath to an image: ")

# Read the image and encode it to base64:
base64_image = ""
try:
    image = open(path.replace("'", ""), "rb").read()
    base64_image = base64.b64encode(image).decode("utf-8")
except:
    print("Couldn't read the image. Make sure the path is correct and the file exists.")
    sys.exit()

completion = client.chat.completions.create(
    model="llava",  # tested with second-state/Llava-v1.5-7B-GGUF llava-v1.5-7b-Q4_K_M.gguf
    #model="model-identifier",
    messages=[
        {
            "role": "system",
            "content": "This is a chat between a user and an assistant. The assistant is helping the user to describe an image.",
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What’s in this image?"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        },
    ],
    max_tokens=1000,
    stream=True,
)

for chunk in completion:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
