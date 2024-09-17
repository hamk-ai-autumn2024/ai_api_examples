import requests
import os

url = "https://api.piapi.ai/api/suno/v1/music"
api_key = os.getenv("PIAPI_KEY")  # Get your API key from https://piapi.ai/
print(api_key)

print("Generating music...")
payload = {
    "custom_mode": True,
    "mv": "chirp-v3-5",
    "input": {
        "prompt": """[Verse 1]
In the quiet of the night,
I still hear the echoes of your name,
Haunted by the memories,
Nothing ever feels the same.

[Pre-Chorus]
And I, can't escape 
The shadows of our fate.

[Chorus]
Aah, I'm lost without your love,
Ooh, Falling through the dark above,
Ooh, In this void, I'm incomplete,
Without you, my world’s obsolete.

[Verse 2]
Every word you said to me,
Is a script of broken dreams,
Carved into my fragile heart,
Now I'm tearing at the seams.
""",
        "title": "Without your love",
        "tags": "R&B",
        "continue_at": 0,
        "continue_clip_id": ""
    }
}
headers = {
    "X-API-Key": "%s" % api_key,
    #"X-API-Key": "{{%s}}" % api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())
