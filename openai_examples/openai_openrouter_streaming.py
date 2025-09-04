from openai import OpenAI
import os

# Assumes you have set the OPENROUTER_API_KEY environment variable
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

stream = client.chat.completions.create(
    model="moonshotai/kimi-k2:free",
    messages=[
        {
            "role": "system", 
            "content": "Answer directly without a preamble."
        },
        {
            "role": "user",
            "content": "List TOP10 most widely spoken languages.",
        },
    ],
    temperature=0.3,
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
