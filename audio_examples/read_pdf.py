from pypdf import PdfReader
import re

# creating a pdf reader object
reader = PdfReader('Robinson_Crusoe_BT.pdf')

# printing number of pages in pdf file
print(f"{len(reader.pages)} pages")

# extracting text from page
full_text = ""
for page in reader.pages:
    page_text = page.extract_text()
    # Convert CR+LF to LF
    page_text = page_text.replace('\r\n', '\n')
    # removing consecutive empty lines
    page_text = re.sub(r'\n{2,}', '\n\n', page_text)
    # removing extra white spaces between words 
    page_text = re.sub(r' +', ' ', page_text)
    # remove "Robinson Crusoe" in the first line only
    page_text = re.sub(r'Robinson Crusoe', '', page_text, 1)
    # remove page numbers "1 of 100"
    page_text = re.sub(r'\d+\s+of\s+\d+', '', page_text)
    page_text = page_text.strip()
    full_text += page_text

# remove consecutive empty lines
print(full_text[:5000])
