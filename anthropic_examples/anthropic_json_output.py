import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    # api_key="my_api_key",
)
message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    system = "Respond directely without any preamble. Output JSON format.",
    messages=[
        {
            "role": "user",
            "content": """List popular recipies in the following format:
[
  {
    "recipe_name": "Name of the recipe",
    "ingredients": [
      "ingredient #1",
      "ingredient #2",
    ],
  },
]
"""
        },
    ]
)
print(message.content[0].text)
