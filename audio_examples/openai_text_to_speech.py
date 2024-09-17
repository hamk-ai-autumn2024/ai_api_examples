from openai import OpenAI
import warnings

# just to get rid of the warnings
#warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

client = OpenAI()  # use the API key from the OPENAI_API_KEY environment variable
speech_file_path = "speech.mp3"
prompt = input("What do you want me to say?")
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy", # alloy, echo, fable, onyx, nova, and shimmer
  input=prompt
)
response.stream_to_file(speech_file_path)
