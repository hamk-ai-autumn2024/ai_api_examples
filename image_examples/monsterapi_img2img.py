from monsterapi import client
import requests
import os              
import json
import mimetypes
# Initialize the client with your API key
api_key = os.getenv("MONSTER_API_KEY")  # set your MONSTER_API_KEY in an environment variable   
monster_client = client(api_key)

filepath = "petri.jpg"

## Monster API File Upload API
url = "https://api.monsterapi.ai/v1/upload"

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {api_key}"
}

file_name = os.path.basename(filepath)
get_file_urls = requests.get(f"{url}?filename={file_name}", headers=headers)

## Extract upload URL and download URL
upload_url = json.loads(get_file_urls.text)['upload_url']
download_url = json.loads(get_file_urls.text)['download_url']

## Upload file to Monster S3 bucket
## Read file content as binary data
data = open(filepath, 'rb').read()

## Create file header using Mime variable
headers = {
    "Content-Type":mimetypes.guess_type(filepath)[0],
}
## Upload file to S3
file_uploaded = requests.put(upload_url,data=data,headers=headers)

print("file_uploaded...")


model = 'img2img'  # Replace with the desired model name
input_data = {
  'prompt': 'old man with eye glasses and beard',
  'init_image_url': download_url, #'https://www.example.com/image_jpeg',  # Replace with your image URL
  'negprompt': 'deformed, bad anatomy, disfigured, poorly drawn face',
  'steps': 30,
  'strength': 0.75,
  'guidance_scale': 7.5,
  'seed': 2414  # -1 for random seed
}
print("Generating image...")
result = monster_client.generate(model, input_data)
print(result['output'])

