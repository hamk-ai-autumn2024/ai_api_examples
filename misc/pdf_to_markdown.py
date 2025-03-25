from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
#result = md.convert("finland.pdf")
result = md.convert("BashTutorial.docx")
print(result.text_content)