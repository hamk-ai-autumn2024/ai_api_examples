import base64
import requests
import os
import sys

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
    "max_tokens": 300,
}

response = requests.post(
    "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
)

print(response.json())
print(response.json().get("choices")[0].get("message").get("content"))
