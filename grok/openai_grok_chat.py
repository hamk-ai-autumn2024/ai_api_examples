from openai import OpenAI
import os

# Point to the local server
client = OpenAI(base_url="https://api.x.ai/v1", api_key=os.getenv("XAI_API_KEY"))

history = [
    {"role": "system", "content": "You will respond briefly and using spoken language what the user uses."},
]
model = "grok-3-mini"  # supports reasoning and is faster than the large model
#model = "grok-3-latest"  # doesn't support reasoning but is more accurate and slower than the mini model

print(f"Chat with {model}. Enter 'exit' or 'quit' to stop the conversation.")
while True:
    prompt = input("> ")
    if prompt == "exit" or prompt == "quit" or len(prompt) == 0:
        break
    history.append({"role": "user", "content": prompt})
    
    completion = client.chat.completions.create(
        model=model,
        reasoning_effort="low", # "low" | "high"
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
