import chainlit as cl
from chainlit import TextInput, Slider

from openai import OpenAI
import os

# Define chat settings
settings = cl.ChatSettings([
    TextInput(
        id="system_prompt",
        label="System Prompt",
        initial="You are a helpful assistant.",
        multiline=True,
    ),
    Slider(
        id="temperature",
        label="Temperature",
        min=0.0,
        max=1.0,
        initial=0.7,
        step=0.1,
    ),
])

@cl.on_settings_update
async def on_settings_update(settings):
    cl.user_session.set("settings", settings)

@cl.on_chat_start
async def on_chat_start():
    await cl.ChatSettings(settings).send()

@cl.on_message
async def on_message(message: cl.Message):
    settings = cl.user_session.get("settings")
    system_prompt = settings.system_prompt
    temperature = settings.temperature

    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    response = client.chat.completions.create(
        model="moonshotai/kimi-k2:free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message.content}
        ],
        temperature=temperature,
        stream=True
    )

    msg = cl.Message(content="")
    await msg.send()

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            msg.content += chunk.choices[0].delta.content
            await msg.update()

    await msg.update()