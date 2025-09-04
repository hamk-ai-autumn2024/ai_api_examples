from openai import OpenAI
client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {
            "role": "user",
            "content": "Say 'double bubble bath' ten times fast.",
        },
    ],
    stream=True,
)

for chunk in stream:
    print(chunk)
    print(chunk.choices[0].delta.content)
    print("****************")