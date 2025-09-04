from openai import OpenAI

client = OpenAI()  # this assumes you have set the OPENAI_API_KEY environment variable

completion = client.chat.completions.create(
    model="gpt-4o-mini",  # Change your model here
    messages=[
        # this is the system prompt
        {"role": "system", "content": "Answer directly without any preamble."},
        {"role": "user", "content": "Explain blood types and their compatibility."},
    ],
    temperature=0.3,
    max_completion_tokens=1000,
    stream=False,  # default, wait until everything is ready
)
text = completion.choices[0].message.content
print(text)

