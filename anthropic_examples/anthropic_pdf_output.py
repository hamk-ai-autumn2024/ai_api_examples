import anthropic
from markdown_pdf import MarkdownPdf, Section

client = anthropic.Anthropic()  # this assumes you have set the ANTHROPIC_API_KEY environment variable

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system = "Respond directly without any preamble. Use markdown formatting.",
    messages=[
        {
            "role": "user",
            "content": "Write a short article about Finland, including a table of most important statistics of the country.",
        },
    ]
)
markdown_text = message.content[0].text
print(markdown_text)

pdf = MarkdownPdf(toc_level=1)
pdf.add_section(Section(markdown_text, paper_size="A4"), user_css="table, td, th {border: 1px solid black;}")
pdf.meta["title"] = "Finland"
pdf.meta["author"] = "Anthropic Claude"
pdf.save("finland.pdf")   # Save the PDF to the current working directory
