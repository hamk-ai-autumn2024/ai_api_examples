from openai import OpenAI
import time

# Point to the local server
# client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
# client = OpenAI(api_key="sk-1234")  # unsafe to hardcode the API key
client = OpenAI()  # this assumes you have set the OPENAI_API_KEY environment variable


print("Generating response...")
start_time = time.time()  # Start timing
completion = client.chat.completions.create(
    model="gpt-4o-mini",  # Change your model here
    messages=[
        # this is the system prompt
        {"role": "system", "content": "Always to your best ability."},
        {"role": "user", "content": "Explain black holes in increasing complexity."},
    ],
    temperature=0.9,
    max_tokens=500,
    # top_p=1,
    # presence_penalty=0.5,
    # frequency_penalty=0.5,
    stream=False,  # default, wait until everything is ready
)
end_time = time.time()  # End timing
print(completion.choices[0].message.content)
print(f"Time elapsed: {end_time - start_time} seconds")
