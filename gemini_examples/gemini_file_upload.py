import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
print("Uploading file...")
input_file = genai.upload_file(path="Robinson_Crusoe_BT.pdf",
                                display_name="Robinson Crusoe PDF")

print(f"Uploaded file '{input_file.display_name}' as: {input_file.uri}")
print("Analyzing...")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
# Prompt the model with text and the previously uploaded image.
response = model.generate_content([input_file, "Summarize the story and list the main characters"])
print(response.text)