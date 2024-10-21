import cohere
import os

api_key = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(api_key=api_key)

# Retrieve the documents
documents = [
  {
    "data": {
      "title": "Tall penguins",
      "snippet": "Emperor penguins are the tallest."
    }
  },
  {
    "data": {
      "title": "Penguin habitats",
      "snippet": "Emperor penguins only live in Antarctica."
    }
  },
  {
    "data": {
      "title": "What are animals?",
      "snippet": "Animals are different from plants."
    }
  }
]

# Add the user message
message = "Where do the tallest penguins live?"
messages = [{"role": "user", "content": message}]

response = co.chat(
    model="command-r-plus",
    messages=messages,
    documents=documents)

print(response.message.content[0].text)

print(response.message.citations)
