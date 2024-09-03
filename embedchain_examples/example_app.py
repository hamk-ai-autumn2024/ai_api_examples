import os
from embedchain import App

# using OpenAI by default
# Replace this with your OpenAI key
#os.environ["OPENAI_API_KEY"] = "sk-xxxx"

app = App()
app.reset()  # Resets the app to start fresh, otherwise it will append to the existing data
app.add("https://www.forbes.com/profile/elon-musk")
app.add("https://en.wikipedia.org/wiki/Elon_Musk")
answer = app.query("What is the net worth of Elon Musk today?")
print(answer)  # Answer: The net worth of Elon Musk today is $239.9 billion.
