import replicate
import time
from file_util import *
import optparse
import sys
import base64

start_time = time.time()

# Parse command line options
usage = "Usage: %prog [options] input_image (url or file path)"
parser = optparse.OptionParser(usage=usage)
parser.add_option("-s", "--scale_factor", dest="scale_factor", default=2, type="int", help="Scale factor for upscaling (default: 2)")
parser.add_option("-f", "--face_enhance", dest="face_enhance", default=False, action="store_true", help="Enable face enhancement (default: False)")
(options, args) = parser.parse_args()

# Get input image URL from command line
if len(args) == 0:
    print("Error: Input image URL is required.")
    sys.exit(1)
input_image = args[0]

if input_image.startswith("http"):
    print(f"Reading image from URL {input_image} ...")
    #image = fetch_url(input_image)
else:
    print(f"Reading image from file {input_image} ...")
    input_image = open(input_image, "rb")

print("Upscaling image...")
output = replicate.run(
    "nightmareai/real-esrgan:f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa",
    input={
        "image": input_image,
        "scale": options.scale_factor,
        "face_enhance": options.face_enhance
    }
)

print(output)

end_time = time.time()
time_consumed = end_time - start_time
print(f"Time consumed: {time_consumed} seconds")
url = output  # the URL of the upscaled image
base_name = url.split("/")[-1]  # find the last part of string after last "/"
base_name = add_prefix_to_filename(base_name, "_upscaled")
image_data = fetch_url(url)
if image_data:
    new_name = find_new_file_name(base_name)
    if save_binary_file(image_data, new_name):
        print(f"Image saved as {new_name}")
    else:
        print("Error saving image")