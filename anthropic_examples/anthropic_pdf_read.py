import anthropic
from pypdf import PdfReader

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    # api_key="my_api_key",
)
prompt = """Generate 10 relatively difficult multiple choices questions based on this text.
Only one correct answer per 5 choices. Show also the correct choice."""
reader = PdfReader('IntroductionToPython3.pdf')
pages  = len(reader.pages)
text = ""
for page in reader.pages:
    text += page.extract_text()

prompt += "\n"+text+"\n"  # Add the text to the prompt and few new lines

with client.messages.stream(
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
    model="claude-sonnet-4-20250514",
) as stream:
  for text in stream.text_stream:
      print(text, end="", flush=True)
