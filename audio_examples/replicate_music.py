import replicate
from file_util import fetch_url, save_binary_file, find_new_file_name
input = {
    "prompt": "chill music with construction vibes sound behind, dominant in piano and synth",
    "duration": 60
}
print("Generating music...")
output = replicate.run(
    "ardianfe/music-gen-fn-200e:96af46316252ddea4c6614e31861876183b59dce84bad765f38424e87919dd85",
    input=input
)
url = output
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
