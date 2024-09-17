import replicate
from file_util import fetch_url, save_binary_file, find_new_file_name

print("Generating audio...")
output = replicate.run(
    "suno-ai/bark:b76242b40d67c76ab6742e987628a2a9ac019e11d56ab96c4e91ce03b79b2787",
    input={
        "prompt": """Hello, my name is Suno. I really like ginger break cookies.
I - uh - know that they are usually only eaten during the holidays, but I think they should be eaten all year round.
Ah, they are just so yummy!""",
        "text_temp": 0.7,
        "output_full": False,
        "waveform_temp": 0.7,
        #"history_prompt": "announcer"
        "history_prompt": "en_speaker_0"
    }
)
url = output["audio_out"]
print(output)
# Download the audio
print("Downloading audio...")
audio_data = fetch_url(url)
# Save the audio wav to a file
print("Saving audio...")
if audio_data is not None:
    file_name = find_new_file_name("out.wav")
    if save_binary_file(data=audio_data, filename=file_name):
      print(f"Audio saved to {file_name}")
