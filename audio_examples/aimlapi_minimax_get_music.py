import requests, os
import json
api_key = os.getenv("AIML_API_KEY") # set your AIML_API_KEY in an environment variable

generation_id = input("AIML generation id?")
def main():
    url = "https://api.aimlapi.com/v2/generate/audio"
    params = {
        "generation_id": f"{generation_id}",
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    print("Generation:", response.json())

if __name__ == "__main__":
    main()