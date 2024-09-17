import requests
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python3 fetch_data.py <task_id>")
    sys.exit(1)
task_id = sys.argv[1] 

api_key = os.getenv("PIAPI_KEY")

url = f"https://api.piapi.ai/api/suno/v1/music/{task_id}"

print("Fetching data from the API...")
headers = {
    "X-API-Key": f"{api_key}",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
data = response.json()

# print the data, which is a bit complex due to nested dictionaries
if data["code"] == 200:
    clips = data["data"]["clips"]
    # iterate over the clips dictionary
    for song_id, song_data in clips.items():
        print(f"Song ID: {song_id}")
        if "audio_url" in song_data:
            print(f"Audio URL: {song_data['audio_url']}")
        if "video_url" in song_data:
            print(f"Video URL: {song_data['video_url']}")
else:
    print(f"Error: {data['code']}")
    