import replicate
import time
from file_util import *

start_time = time.time()
input_image = open("out-0_3.png", "rb")
print("Upscaling image...")
output = replicate.run(
    "philz1337x/clarity-upscaler:dfad41707589d68ecdccd1dfa600d55a208f9310748e44bfe35b4a6291453d5e",
    #"nightmareai/real-esrgan:f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa",
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
for index, item in enumerate(output):
    with open(f"upscale_{index}.png", "wb") as file:
        file.write(item.read())

