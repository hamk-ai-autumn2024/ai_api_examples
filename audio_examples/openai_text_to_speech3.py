from openai import OpenAI
import soundfile as sf
import sounddevice as sd
import io

client = OpenAI()  # use the API key from the OPENAI_API_KEY environment variable
speech_file_path = "speech.mp3"
prompt = input("What do you want me to say?")

spoken_response = client.audio.speech.create(
    model="tts-1-hd",
    voice="fable",
    response_format="opus", # opus, aac, mp3, wav, flac
    input=prompt,
)
print("Streaming the response...")
buffer = io.BytesIO()  # this is a buffer to store the audio data
for chunk in spoken_response.iter_bytes(chunk_size=4096):
    buffer.write(chunk)
buffer.seek(0)  # Reset the buffer to the beginning
print("Playing the response...")
with sf.SoundFile(buffer, "r") as sound_file:
    data = sound_file.read(dtype="int16")
    sd.play(data, sound_file.samplerate)
    sd.wait()  # Wait until the file is done playing
