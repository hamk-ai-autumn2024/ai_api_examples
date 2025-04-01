import replicate
import time
from file_util import *
import optparse
import sys
import base64
import argparse

start_time = time.time()

# Parse command line options
usage = """Usage: %prog [options] input_image (url or file path)
Upscale an image using Real-ESRGAN. The input image can be a URL or a local file path.
Upscale 2x by default. Face enhancement is not enabled by default."""
parser = argparse.ArgumentParser(prog="replicate_upscale_opt.py", description=usage)
parser.add_argument("-s", "--scale_factor", dest="scale_factor", default=2, type=int, help="Scale factor for upscaling (default: 2)")
parser.add_argument("-f", "--face_enhance", dest="face_enhance", default=False, action="store_true", help="Enable face enhancement (default: False)")
parser.add_argument("files", nargs=1, help="Input image URL or file path")
args = parser.parse_args()

# Get input image URL from command line
#if len(args) == 0:
#    print("Error: Input image URL is required.")
#    sys.exit(1)
#input_image = args[0]

input_image = args.files[0]

if input_image.startswith("http"):
    print(f"Reading image from URL {input_image} ...")
    #image = fetch_url(input_image)
else:
    print(f"Reading image from file {input_image} ...")
    input_image = open(input_image, "rb")

print("Upscaling image...")
output = replicate.run(
    #"philz1337x/clarity-upscaler:dfad41707589d68ecdccd1dfa600d55a208f9310748e44bfe35b4a6291453d5e",
    "nightmareai/real-esrgan:f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa",
    input={
        "image": input_image,
        "scale": args.scale_factor,
        "face_enhance": args.face_enhance
    }
)

print(output)

end_time = time.time()
time_consumed = end_time - start_time
print(f"Time consumed: {time_consumed} seconds")
print("Reading image data...")
image_data = output.read()
output_file_name = find_new_file_name("upscale.png")
save_binary_file(image_data, output)
print(f"Image saved as: {output_file_name}")
