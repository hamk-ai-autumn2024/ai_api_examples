from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio") # Point to the local server
# client = OpenAI()  # this assumes you have set the OPENAI_API_KEY environment variable
# Tested with LWDCLS/DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored-GGUF-IQ-Imatrix-Request
# DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored-Q4_K_M-imat.gguf

person = input("Whom do you want to roast?")
history = [
    {"role": "system", "content": """You are a politically incorrect standup comedian.
You are not afraid to use curse words or vulgar things. You roast the given topic in the nastiest possible ways.
You will be paid well for creativity"""},
    {"role": "user", "content": person},
]

while True:
    completion = client.chat.completions.create(
        model="gpt-4o-mini", # Change your model here
        messages=history,
        temperature=0.9,
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
    