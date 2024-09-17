import replicate
from file_util import fetch_url, save_binary_file, find_new_file_name

print("Generating music...")
output = replicate.run(
    "meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
    input={
        "top_k": 250,
        "top_p": 0,
        "prompt": "Epic cinematic orchestral music for a fantasy movie",
        "duration": 15,  # in seconds
        "temperature": 1,
        "continuation": False,
        "model_version": "stereo-large",
        "output_format": "mp3",
        "continuation_start": 0,
        "multi_band_diffusion": False,
        "normalization_strategy": "peak",
        "classifier_free_guidance": 3
    }
)
print(output)
url = output # output is the URL of the generated audio

# Download the audio
print("Downloading audio...")
audio_data = fetch_url(url)
# Save the audio to a file
print("Saving audio...")
if audio_data is not None:
    file_name = find_new_file_name("out.mp3")
    if save_binary_file(data=audio_data, filename=file_name):
      print(f"Audio saved to {file_name}")
