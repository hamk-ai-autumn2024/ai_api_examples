import anthropic
import base64
import httpx

# Max 5 MB image
image1_url = "https://upload.wikimedia.org/wikipedia/commons/d/d4/Helsinki_University_of_Technology_auditorium.jpg"
image1_media_type = "image/jpeg"
image1_data = base64.b64encode(httpx.get(image1_url).content).decode("utf-8")

import anthropic

client = anthropic.Anthropic()  # assumes ANTHROPIC_API_KEY is set in the environment
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system = "Respond directely without any preamble.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image1_media_type,
                        "data": image1_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ],
        }
    ],
)
print(message.content[0].text)