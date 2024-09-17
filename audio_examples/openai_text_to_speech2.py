from openai import OpenAI

client = OpenAI()  # use the API key from the OPENAI_API_KEY environment variable
speech_file_path = "speech.mp3"
prompt = input("What do you want me to say?")
with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input=prompt
    ) as  response:
        response.stream_to_file(speech_file_path)
