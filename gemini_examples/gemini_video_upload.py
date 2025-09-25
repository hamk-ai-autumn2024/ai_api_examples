import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
print("Uploading file...")
input_file = genai.upload_file("sample_video.mp4", display_name="Sample Video")

print(f"Uploaded file '{input_file.display_name}' as: {input_file.uri}")
print("Analyzing...")
model = genai.GenerativeModel(model_name="gemini-2.5-flash")
# Prompt the model with text and the previously uploaded image.
response = model.generate_content([input_file, "What is happening in this video? Describe the main character"])

print(response.text)
