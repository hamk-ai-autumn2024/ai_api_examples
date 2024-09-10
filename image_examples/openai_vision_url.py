from openai import OpenAI

client = OpenAI()  # set your OPENAI_API_KEY in an environment variable

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What’s in this image?"},
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Nuuksio_peat_accumulations.jpg",
          },
        },
      ],
    }
  ],
  max_tokens=300,
)
#print(response.choices[0])
print(response.choices[0].message.content)