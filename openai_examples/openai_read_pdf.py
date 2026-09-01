from pathlib import Path

from markitdown import MarkItDown
from openai import OpenAI

pdf_path = Path(__file__).with_name("markitdown_example.pdf")
document = MarkItDown().convert(pdf_path).text_content

client = OpenAI()
result = client.responses.create(
    model="gpt-5.6-luna",
    input=(
        "Summarize the following PDF in exactly two sentences. "
        "Output only the summary.\n\n"
        f"{document}"
    ),
)

print(result.output_text)
