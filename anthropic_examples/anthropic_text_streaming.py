import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    # api_key="my_api_key",
)
prompt = "Write song lyrics about a person who is in love with a robot. Make chorus catchy and rhyming, verses emotional."
with client.messages.stream(
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
    model="claude-sonnet-4-20250514",
) as stream:
  for text in stream.text_stream:
      print(text, end="", flush=True)
