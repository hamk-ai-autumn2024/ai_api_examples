from openai import AsyncOpenAI
import chainlit as cl

client = AsyncOpenAI()

# Instrument the OpenAI client
cl.instrument_openai()

MODEL = "gpt-6-luna"
SYSTEM_PROMPT = "Reply in a concise and direct manner, unless requested otherwise."
TEMPERATURE = 0.7


@cl.on_chat_start
async def start_chat():
    cl.user_session.set(
        "messages",
        [{"role": "system", "content": SYSTEM_PROMPT}],
    )

@cl.on_message
async def on_message(message: cl.Message):
    messages = cl.user_session.get("messages") or []
    messages.append({"role": "user", "content": message.content})

    response = await client.chat.completions.create(
        model=MODEL,
        #temperature=TEMPERATURE,
        messages=messages,
        stream=True,
    )

    response_message = cl.Message(content="")
    async for chunk in response:
        token = chunk.choices[0].delta.content
        if token:
            await response_message.stream_token(token)

    await response_message.send()
    messages.append({"role": "assistant", "content": response_message.content})
    cl.user_session.set("messages", messages)