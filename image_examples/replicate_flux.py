import replicate
import time
from file_util import fetch_url, save_binary_file, find_new_file_name

start_time = time.time()

print("Generating image...")
output = replicate.run(
    #"pwntus/flux-albert-einstein:2ed2f6d1a8563caa2cfada419dffc68b52881bab9bac30c0b8cbe05a4dcae0e5",
    #"bingbangboom-lab/flux-dreamscape:b761fa16918356ee07f31fad9b0d41d8919b9ff08f999e2d298a5a35b672f47e",
    "black-forest-labs/flux-dev",
    input={
        "model": "dev",
        #"prompt": "Happy Einstein in a party, surrounded by female scientists and confetti. He is smiling and holding a glass",
        #"prompt": "calm and peaceful landscape with a small house in the middle of a field of flowers and a clear blue sky",
        "prompt": 'a slim programmer wearing eye glasses and a t-shirt with the text "FLUX" on it',
        "lora_scale": 1,
        "num_outputs": 1,
        #"aspect_ratio": "1:1",
        "aspect_ratio": "16:9",
        "output_format": "png",
        "guidance_scale": 3.5,
        "output_quality": 90,
        "prompt_strength": 0.8,
        "extra_lora_scale": 0.8,
        "num_inference_steps": 35
    }
)

end_time = time.time()
time_consumed = end_time - start_time
print(f"Time consumed: {time_consumed} seconds")
url = output[0]
print(url)
base_name = url.split("/")[-1]  # find the last part of string after last "/"
image_data = fetch_url(url)
if image_data:
    new_name = find_new_file_name(base_name)
    if save_binary_file(image_data, new_name):
        print(f"Image saved as {new_name}")
    else:
        print("Error saving image")
