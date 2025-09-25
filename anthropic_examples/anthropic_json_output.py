import anthropic
import json

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    # api_key="my_api_key",
)
message = client.messages.create(
  model="claude-sonnet-4-20250514",
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

json_text = message.content[0].text
print(json_text)
try:
    json_obj = json.loads(json_text)
    json_formatted = json.dumps(json_obj, indent=4)
    print(json_formatted)
except json.JSONDecodeError as e:
    print("Error decoding JSON:", e)


