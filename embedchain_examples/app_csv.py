import os
from embedchain import App

# Defaults are read from config.yaml
# You can also set the API key here
# using OpenAI by default
# Replace this with your OpenAI key
#os.environ["OPENAI_API_KEY"] = "sk-xxxx"

app = App()
app.reset()  # Resets the app to start fresh, otherwise it will append to the existing data
app.add('username-or-email.csv', data_type='csv')
answer = app.query("Summarize")
print(answer)
