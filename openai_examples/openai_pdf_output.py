from openai import OpenAI
from markdown_pdf import MarkdownPdf, Section

client = OpenAI()  # this assumes you have set the OPENAI_API_KEY environment variable

completion = client.chat.completions.create(
    model="gpt-4o",  # Change your model here
    messages=[
        # this is the system prompt
        {"role": "system", "content": "Answer directly without any preamble. Use markdown formatting."},
        {"role": "user", "content": "Write a short article about Finland, including a table of most important statistics of the country."},
    ],
    temperature=0.9,
    max_tokens=1000,
    stream=False,  # default, wait until everything is ready
)
markdown_text = completion.choices[0].message.content
print(markdown_text)

pdf = MarkdownPdf(toc_level=1)
pdf.add_section(Section(markdown_text, paper_size="A4"), user_css="table, td, th {border: 1px solid black;}")
pdf.meta["title"] = "Finland"
pdf.meta["author"] = "OpenAI"
pdf.save("finland.pdf")   # Save the PDF to the current working directory
