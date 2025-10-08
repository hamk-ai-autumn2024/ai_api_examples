from xai_sdk import Client
from xai_sdk.chat import system, user, assistant
import os

# Point to the local server
client = Client(api_key=os.getenv("XAI_API_KEY"),
                timeout=3600 # longer timeout for reasoning models
                )

history = [system("You will respond briefly and using spoken language what the user uses.")]

model = "grok-4-fast-non-reasoning"

print(f"Chat with {model}. Enter 'exit' or 'quit' to stop the conversation.")
while True:
    prompt = input("> ")
    if prompt == "exit" or prompt == "quit" or len(prompt) == 0:
        break
    history.append(user(prompt))
    
    chat = client.chat.create(
        model=model,
        messages=history,
        temperature=0.7,
    )

    new_message = {"role": "assistant", "content": ""}
    

    for response, chunk in chat.stream():
        print(chunk.content, end="", flush=True) # Each chunk's content
        #print(response.content, end="", flush=True) # The response object auto-accumulates the chunks
    
    history.append(assistant(response.content))
    print()
