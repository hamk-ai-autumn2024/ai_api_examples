import google.generativeai as genai
import os
import json

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

prompt = """List a few popular cookie recipes in JSON format.

Use this JSON schema:

Recipe = {'recipe_name': str, 'ingredients': list[str]}
Return: list[Recipe]"""

model = genai.GenerativeModel('gemini-2.5-flash',
                              generation_config={"response_mime_type": "application/json"})
result = model.generate_content(prompt)
#print(result.text)

json_obj = json.loads(result.text)
json_formatted = json.dumps(json_obj, indent=4)
print(json_formatted)

