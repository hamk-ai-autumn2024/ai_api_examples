import os
import requests
from openai import OpenAI

#api_key = os.getenv("AIMLAPI_API_KEY") # set your AIMLAPI_API_KEY in an environment variable
#api = OpenAI(api_key=api_key, base_url="https://api.aimlapi.com/v1")

print("Generating music...")
response = requests.post(
    "https://api.aimlapi.com/generate",
    headers={"Content-Type":"application/json",
            "Authorization": f"Bearer {api_key}",
            },
        json={
            "prompt":"energetic eurodance, female vocals", 
            "make_instrumental": False, # True to remove vocals
            "wait_audio": True # True to wait for audio generation
            }
)
data = response.json()
print(data)