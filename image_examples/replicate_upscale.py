import replicate
import time
from file_util import *

start_time = time.time()
input_image = open("out-0_3.png", "rb")
print("Upscaling image...")
output = replicate.run(
    "nightmareai/real-esrgan:f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa",
    input={
        "image": input_image,
        #"image": "https://replicate.delivery/yhqm/IqmpNq05kBbcIJAiZrtO01POvF8S04A2NNPHGrMsZ3fJs6sJA/out-0.png",
        "scale": 2,
        "face_enhance": False
    }
)
print(output)

end_time = time.time()
time_consumed = end_time - start_time
print(f"Time consumed: {time_consumed} seconds")
url = output
print(url)
base_name = url.split("/")[-1]  # find the last part of string after last "/"
base_name = add_prefix_to_filename(base_name, "_upscaled")
image_data = fetch_url(url)
if image_data:
    new_name = find_new_file_name(base_name)
    if save_binary_file(image_data, new_name):
        print(f"Image saved as {new_name}")
    else:
        print("Error saving image")
