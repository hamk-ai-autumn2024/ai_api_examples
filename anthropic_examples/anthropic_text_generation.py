import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    # api_key="my_api_key",
)
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system = "Respond directely without any preamble.",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of Finland and its population?",
            #"content": "Generate Python to check if given string is palindrome. Handle spaces and special characters."
        },
    ]
)
#print(message.content)
print(message.content[0].text)
