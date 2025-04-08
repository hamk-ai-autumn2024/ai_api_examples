import os
import requests
from openai import OpenAI

api_key = os.getenv("AIML_API_KEY") # set your AIML_API_KEY in an environment variable

def main():
    url = "https://api.aimlapi.com/v2/generate/audio"
    payload = {
        "model": "minimax-music",
        "prompt": "## Fast and Limitless. In the heart of the code, where dreams collide, FALs the name, taking tech for a ride. Generative media, blazing the trail, Fast inference power, we'll never fail.##",
        "reference_audio_url": "https://cdn.aimlapi.com/squirrel/files/zebra/WzNbqH7vR20MNTOD1Ec7k_output.mp3",
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    print("Generation:", response.json())

if __name__ == "__main__":
    main()


