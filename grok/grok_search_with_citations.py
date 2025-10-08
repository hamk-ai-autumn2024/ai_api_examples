import os
from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.search import SearchParameters

client = Client(api_key=os.getenv("XAI_API_KEY"))

chat = client.chat.create(
    model="grok-4",
    search_parameters=SearchParameters(
        mode="auto",
        return_citations=True,
        max_search_results=5,
    ),
)
chat.append(user("Provide me a digest of world of AI news on October 2025."))

response = chat.sample()
print(response.content)
print("\nCitations:")
for citation in response.citations:
    print(f"- {citation}")
