from google import genai
from google.genai import types
import os 
import json

prompt = """List 3 popular cookie recipes in JSON format.

Use this JSON schema:

Recipe = {'recipe_name': str, 'ingredients': list[str]}
Return: list[Recipe]"""

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction=[
            "Output should be in valid JSON format with no additional text. No markdown formatting, no JSON code blocks.",
        ]
    ),
)
print(response.text)
# parse and pretty print the JSON response
json_obj = json.loads(response.text)
json_formatted = json.dumps(json_obj, indent=4)
print(json_formatted)

