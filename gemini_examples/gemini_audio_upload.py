import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
print("Uploading file...")
input_file = genai.upload_file("petri_speech_sample.wav", display_name="Sample Audio")

print(f"Uploaded file '{input_file.display_name}' as: {input_file.uri}")
print("Analyzing...")
model = genai.GenerativeModel(model_name="gemini-2.0-flash")
# Prompt the model with text and the previously uploaded image.
response = model.generate_content([input_file, "Transcribe the audio file. Then translate into Finnish"])

print(response.text)
