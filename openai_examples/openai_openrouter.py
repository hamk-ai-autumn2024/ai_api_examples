from openai import OpenAI
import os

# Assumes you have set the OPENROUTER_API_KEY environment variable
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

history = [
#    {"role": "system", "content": "You will respond briefly and using spoken language what the user uses."},
    {"role": "system", "content": "You are a cartoon pirate and you always stay in your role."},
]
model = "deepseek/deepseek-chat-v3.1:free"
#model = "mistralai/mistral-nemo:free"  # model name for OpenRouter
#model = "google/gemini-2.0-flash-exp:free"
model = "qwen/qwen3-30b-a3b:free"  # model name for OpenRouter
model = "moonshotai/kimi-k2:free"

print(f"Chat with {model}. Enter 'exit' or 'quit' to stop the conversation.")
while True:
    prompt = input("> ")
    if prompt == "exit" or prompt == "quit" or len(prompt) == 0:
        break
    history.append({"role": "user", "content": prompt})
    
    completion = client.chat.completions.create(
        model=model,
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
