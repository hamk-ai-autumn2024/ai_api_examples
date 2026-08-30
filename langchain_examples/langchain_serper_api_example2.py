from langchain_community.utilities import GoogleSerperAPIWrapper

# Assumes that SERPER_API_KEY is set in the environment 
# Note that SERPER_API_KEY must be the serper dev api key https://serper.dev/api-key

search = GoogleSerperAPIWrapper()
results = search.run("Who invented Python programming language?")
print(results)
