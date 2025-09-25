from google import genai
from markdown_pdf import MarkdownPdf, Section
import os 

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

prompt = "Write about Finland, including table of most important statistics of the country."
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)
print(response.text)

pdf = MarkdownPdf(toc_level=1)
pdf.add_section(Section(response.text, paper_size="A4"), user_css="table, td, th {border: 1px solid black;}")
pdf.meta["title"] = "Finland"
pdf.meta["author"] = "Google Gemini"
pdf.save("finland.pdf")   # Save the PDF to the current working directory


