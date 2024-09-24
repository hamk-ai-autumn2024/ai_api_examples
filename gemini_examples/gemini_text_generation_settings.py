import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

#model = genai.GenerativeModel("gemini-1.5-pro")
generation_config = {
    "temperature": 0.8,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = {
    # Removing all blocks  for the sake of testing
    # BLOCK_NONE, BLOCK_ONLY_HIGH, BLOCK_MEDIUM_AND_ABOVE, BLOCK_LOW_AND_ABOVE, HARM_BLOCK_THRESHOLD_UNSPECIFIED
    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
}
system_prompt = "Respond directly without any small talk or preambles."

model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config, safety_settings=safety_settings,
                              system_instruction=system_prompt)

# test the model, can it generate a joke with safety settings turned off
response = model.generate_content("Tell a joke about a middle-aged female programmer", stream=False)
print(response.text)
