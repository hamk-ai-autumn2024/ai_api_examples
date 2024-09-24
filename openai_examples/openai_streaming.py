from openai import OpenAI

# Point to the local server
# client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
# client = OpenAI(api_key="sk-1234")  # unsafe to hardcode the API key
client = OpenAI()  # this assumes you have set the OPENAI_API_KEY environment variable

completion = client.chat.completions.create(
    model="gpt-4o", # Change your model here
    messages=[
        # this is the system prompt
        {"role": "system", "content": "Always to your best ability."},

        {"role": "user", "content": "Selitä esimerkein suomen kielen adjektiivien vertailumuodot."}
    ],
    temperature=0.9,
    max_tokens=500,
    # top_p=1,
    # presence_penalty=0.5,
    # frequency_penalty=0.5,
    stream=True # stream the response
)

for chunk in completion:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
