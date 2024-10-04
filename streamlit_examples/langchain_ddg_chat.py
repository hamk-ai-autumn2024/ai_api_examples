import streamlit as st
from langchain import hub
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_openai import OpenAI, ChatOpenAI

# You should set up OPENAI_API_KEY and LANGCHAIN_API_KEY in your environment variables
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3, streaming=True)
#model = OpenAI(temperature=0.5, streaming=True)
tools = load_tools(["ddg-search"])
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def init_chat():
    st.session_state["messages"] = [
        {"role": "system", "content": "Respond directly without any preamble. Give numerical data and facts if possible."},
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

with st.sidebar:
    if clear_chat := st.button("Clear Chat"):
        init_chat()

if "messages" not in st.session_state:
    init_chat()

for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        output = agent_executor.invoke({"input": prompt}, {"callbacks": [st_callback]})
        response = output["output"]
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)

