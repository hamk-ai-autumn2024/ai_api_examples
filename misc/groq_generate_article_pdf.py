import os
import time
import sys
from groq import Groq
from markdown_pdf import MarkdownPdf, Section

start_time = time.time()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

if len(sys.argv) > 1:
    topic = sys.argv[1]
else:
    topic = "Importance of fast language models"
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": """Generate long comprehensive article on given topic, including concrete practical
examples and references in APA style. Respond directly without preamble in markdown format.""",
        },
        {
            "role": "user",
            "content": topic,
        }
    ],
    model="llama-3.1-8b-instant",
    #model="llama3-8b-8192",
)

end_time = time.time()
time_spent = (end_time - start_time) * 1000  # Convert to milliseconds
markdown_text = chat_completion.choices[0].message.content
print(markdown_text)
print(f"Time spent: {time_spent:.2f} ms")

pdf = MarkdownPdf(toc_level=1)
pdf.add_section(Section(markdown_text, paper_size="A4"), user_css="table, td, th {border: 1px solid black;}")
pdf.meta["title"] = topic
pdf.meta["author"] = "Llama-3.1-8b"
pdf.save("article.pdf")   # Save the PDF to the current working directory
