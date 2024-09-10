from monsterapi import client
import os
import regutil
from file_util import fetch_url, save_binary_file, find_new_file_name
import time

# Initialize the client with your API key
#api_key = 'your-api-key'  # Replace 'your-api-key' with your actual Monster API key
api_key = os.getenv("MONSTER_API_KEY")  # set your MONSTER_API_KEY in an environment variable
monster_client = client(api_key)

model = 'sdxl-base' 
# Replace with the desired model name
input_data = {
  'prompt': 'photo of beautiful elf sorceress casting a spell in a fantasy setting',  # text prompt
  'negprompt': 'unreal, fake, meme, joke, disfigured, poor quality, bad, ugly',
  'samples': 2,  # number of images to generate
  'enhance': True,  
  'optimize': True,
  'safe_filter': False,  # allow NSFW content
  'steps': 50,  # more steps can improve quality, but increase processing time
  'aspect_ratio': 'square',
  'guidance_scale': 7.5,
  'seed': -1,  # random
}
print("Generating image...")
results = monster_client.generate(model, input_data)
start_time = time.time()

for url in results['output']:
    print(url)
    image_data = fetch_url(url)
    # Save the image to a file
    if image_data is not None:
        file_name = find_new_file_name(f"monsterapi_.png")
        if save_binary_file(data=image_data, filename=file_name):
                print(f"Image saved to {file_name}")

elapsed_time = time.time() - start_time
print(f"Time consumed: {elapsed_time} seconds")
