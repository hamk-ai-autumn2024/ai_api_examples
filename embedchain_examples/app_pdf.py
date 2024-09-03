import os
from embedchain import App

# using OpenAI by default
# Replace this with your OpenAI key
# os.environ["OPENAI_API_KEY"] = "sk-xxxx"

app = App()
app.reset()  # Resets the app to start fresh, otherwise it will append to the existing data
app.add("https://www.sandylands.lancs.sch.uk/wp-content/uploads/2020/11/the-tortoise-and-the-hare-story.pdf", data_type='pdf_file')
#app.add("Best_of_AI.pdf" , data_type='pdf_file')
#answer, citations = app.query("Summarize. What AI tools did it recommend?", citations=True)
answer, citations = app.query("Summarize. What did we learn?", citations=True)
print(answer)
print(f"Citations:\n{citations}")

