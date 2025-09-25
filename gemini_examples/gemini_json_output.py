from google import genai
from pydantic import BaseModel
import json
import os

class Recipe(BaseModel):
    recipe_name: str
    ingredients: list[str]

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="List 3 popular cookie recipes, and include the amounts of ingredients.",
    config={
        "response_mime_type": "application/json",
        "response_schema": list[Recipe],
    },
)
# Use the response as a JSON string.
json_obj = json.loads(response.text)
json_formatted = json.dumps(json_obj, indent=4)
print(json_formatted)

# Use instantiated objects.
my_recipes: list[Recipe] = response.parsed
for recipe in my_recipes:
    print(f"Recipe: {recipe.recipe_name}")
    print("Ingredients:")
    for ingredient in recipe.ingredients:
        print(f" - {ingredient}")
    print()
