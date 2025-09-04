from openai import OpenAI
client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {
            "role": "user",
            "content": "List TOP10 most widely spoken languages.",
        },
    ],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
    #print(chunk)
    #print(chunk.choices[0].delta.content)
    #print("****************")