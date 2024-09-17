from openai import OpenAI
import sounddevice as sd
import numpy as np
import wavio

fs = 44100  # Sample rate
seconds = 10  # Duration of recording
print ("Recording...")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
print ("Recording done")
wavio.write("speech.wav", myrecording, fs, sampwidth=2)

print ("Transcribing...")
client = OpenAI()  # use the API key from the OPENAI_API_KEY environment variable
audio_file= open("speech.wav", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)
