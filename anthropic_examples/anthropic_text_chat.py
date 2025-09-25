import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    # api_key="my_api_key",
)
messages = []
while True:
    prompt = input("> ").strip()
    if prompt.lower() == "exit" or prompt.lower() == "quit" or len(prompt) == 0:
        break
    messages.append({"role": "user", "content": prompt})
    with client.messages.stream(
        max_tokens=4096,
        messages=messages,
        system = "Answer directly without any preamble. Answer even if you are not sure or the answer would be controversial.",
        model="claude-sonnet-4-20250514",
    ) as stream:
        text = ""
        for chunk in stream.text_stream:
            text += chunk
            print(chunk, end="", flush=True)
        messages.append({"role": "assistant", "content": text})
    print(flush=True)

