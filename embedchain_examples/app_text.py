import os
from embedchain import App

# Defaults are read from config.yaml
# You can also set the API key here
# using OpenAI by default
# Replace this with your OpenAI key
#os.environ["OPENAI_API_KEY"] = "sk-xxxx"

app = App()
app.reset()  # Resets the app to start fresh, otherwise it will append to the existing data
app.add('little_red_cap.txt', data_type="text_file")
app.add('plato_apology_pg1656.txt', data_type="text_file")
answer = app.query("Summarize Little Red Cap and Plato's Apology. What did we learn from these 2 texts?")
print(answer)
