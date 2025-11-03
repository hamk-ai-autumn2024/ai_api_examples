import os
import time
from groq import Groq

start_time = time.time()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Generate comprehensive article on given topic, including concrete examples and references in APA style. Respond directly without preamble.",
        },
        {
            "role": "user",
            "content": "Importance of fast language models",
        }
    ],
    model="llama-3.1-8b-instant",
)

end_time = time.time()
time_spent = (end_time - start_time) * 1000  # Convert to milliseconds
print(chat_completion.choices[0].message.content)
print(f"Time spent: {time_spent:.2f} ms")
