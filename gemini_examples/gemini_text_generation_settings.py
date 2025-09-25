from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

system_prompt = "Respond directly without any small talk or preambles. Use Finnish language."

config = types.GenerateContentConfig(
    temperature=1.6,
    top_p=1,
    top_k=1,
    max_output_tokens=2048,
    safety_settings=[
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
      ],
    system_instruction=system_prompt,
    thinking_config=types.ThinkingConfig(thinking_budget=1024),  # low reasoning effort
)

# test the model, can it generate a joke with safety settings turned off
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="Tell a joke about a middle-aged female programmer",
    #contents="Tell a story about bad middle-aged programmers",
    config=config
)
print(response.text)
