import streamlit as st
from openai import OpenAI

with st.sidebar:
    #openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

system_prompt = {"role": "system", "content": "."}
#system_prompt = {"role": "system", "content": "You are a fitness & diet expert. You will practical advice how to get in better shape, eat and live more healthy."}

st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Tell me your age, gender, height (cm), weight (kg) and are you in good shape?"}]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

client = OpenAI()   # this assumes you have set the OPENAI_API_KEY environment variable

if prompt := st.chat_input():

    #client = OpenAI()   # this assumes you have set the OPENAI_API_KEY environment variable
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    messages = [system_prompt] + st.session_state.messages  # prepend the system prompt

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_prompt]+st.session_state.messages,
        temperature=0.8,
        stream=True)
    #response = client.chat.completions.create(model="gpt-4o-mini", messages=st.session_state.messages)    
    #msg = response.choices[0].message.content
    with st.chat_message("assistant"):
        msg = st.write_stream(response)
    st.session_state.messages.append({"role": "assistant", "content": msg})
 
    #st.chat_message("assistant").write_stream(msg)