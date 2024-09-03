from openai import OpenAI

# Point to the local server
# client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
# client = OpenAI(api_key="sk-1234")  # unsafe to hardcode the API key
client = OpenAI()  # this assumes you have set the OPENAI_API_KEY environment variable

history = [
    {"role": "system", "content": "You will respond briefly and using spoken language what the user uses."},
    {"role": "user", "content": "Hello, introduce yourself"},
]

while True:
    completion = client.chat.completions.create(
        model="gpt-4o-mini", # Change your model here
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    
    print()
    prompt = input("> ")
    if prompt == "exit" or prompt == "quit" or len(prompt) == 0:
        break
    history.append({"role": "user", "content": prompt})
    
