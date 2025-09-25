import google.generativeai as genai
import os
import typing_extensions as typing
import json

class Recipe(typing.TypedDict):
    recipe_name: str
    ingredients: list[str]

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")
result = model.generate_content(
    "List a few popular cookie recipes.",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=list[Recipe]
    ),
)
#print(result.text)
json_obj = json.loads(result.text)
json_formatted = json.dumps(json_obj, indent=2)
print(json_formatted)
