import os
from embedchain import App
import urllib.request
import json

# Defaults are read from config.yaml
# You can also set the API key here
# using OpenAI by default
# Replace this with your OpenAI key
# os.environ["OPENAI_API_KEY"] = "sk-xxxx"

url = "https://jsonplaceholder.typicode.com/users"

try:
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        # print(data)
        app = App()
        app.reset()  # Resets the app to start fresh, otherwise it will append to the existing data
        app.add(json.dumps(data), data_type="json")
        answer = app.query("Summarize")
        print(answer)
except urllib.error.URLError as e:
    print(f"Failed to load JSON from URL: {e.reason}")
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
