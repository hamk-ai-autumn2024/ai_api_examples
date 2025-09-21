import chainlit as cl
import openai
import os
from typing import Optional

# Configure OpenAI client for OpenRouter
client = openai.AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Default settings
DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant."
DEFAULT_TEMPERATURE = 0.7

@cl.on_chat_start
async def start():
    # Initialize settings in user session
    cl.user_session.set("system_prompt", DEFAULT_SYSTEM_PROMPT)
    cl.user_session.set("temperature", DEFAULT_TEMPERATURE)
    cl.user_session.set("model", "moonshotai/kimi-k2:free")
    # Initialize chat history with system prompt
    cl.user_session.set(
        "messages",
        [{"role": "system", "content": DEFAULT_SYSTEM_PROMPT}]
    )
    
    # Create side panel settings
    settings = await cl.ChatSettings([
        cl.input_widget.Select(
            id="model",
            label="Model",
            values=[
                "deepseek/deepseek-chat-v3.1:free",
                "deepseek/deepseek-r1-0528:free",
                "x-ai/grok-4-fast:free",
                "qwen/qwen3-coder:free",
                "qwen/qwen3-235b-a22b:free",
                "qwen/qwen3-30b-a3b:free",
                "moonshotai/kimi-k2:free",
                "google/gemini-2.0-flash-exp:free",
            ],
            initial_index=6,
            description="Choose the model to use"
        ),
        cl.input_widget.TextInput(
            id="system_prompt",
            label="System Prompt",
            initial=DEFAULT_SYSTEM_PROMPT,
            description="Set the system prompt for the AI assistant",
            multiline=True
        ),
        cl.input_widget.Slider(
            id="temperature",
            label="Temperature",
            initial=DEFAULT_TEMPERATURE,
            min=0.0,
            max=1.0,
            step=0.1,
            description="Controls randomness in responses"
        )
    ]).send()

@cl.on_settings_update
async def setup_agent(settings):
    # Update session settings when user changes them
    cl.user_session.set("system_prompt", settings["system_prompt"])
    cl.user_session.set("temperature", settings["temperature"])
    cl.user_session.set("model", settings["model"])
    # Ensure the first message in history is the updated system prompt
    messages = cl.user_session.get("messages") or []
    if not messages:
        messages = [{"role": "system", "content": settings["system_prompt"]}]
    elif messages[0].get("role") == "system":
        messages[0]["content"] = settings["system_prompt"]
    else:
        messages.insert(0, {"role": "system", "content": settings["system_prompt"]})
    cl.user_session.set("messages", messages)

@cl.on_message
async def main(message: cl.Message):
    # Get current settings
    temperature = cl.user_session.get("temperature")
    model = cl.user_session.get("model") or "moonshotai/kimi-k2:free"
    
    # Retrieve and append to chat history
    messages = cl.user_session.get("messages") or []
    if not messages:
        # Fallback safety: seed with current system prompt
        messages = [{"role": "system", "content": cl.user_session.get("system_prompt") or DEFAULT_SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": message.content})
    
    # Create streaming response
    msg = cl.Message(content="")
    
    try:
        # Stream response from OpenRouter
        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True
        )
        
        assistant_content = ""
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                assistant_content += token
                await msg.stream_token(token)
        
        await msg.send()
        
        # Append assistant response to history
        messages.append({"role": "assistant", "content": assistant_content})
        cl.user_session.set("messages", messages)
        
    except Exception as e:
        await cl.Message(content=f"Error: {str(e)}").send()
