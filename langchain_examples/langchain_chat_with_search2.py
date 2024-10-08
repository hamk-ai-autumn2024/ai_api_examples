import streamlit as st
from langchain.agents import AgentExecutor, create_tool_calling_agent
#from langchain.agents import initialize_agent, AgentType, SearchReactDescriptionAgent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_core.tools import tool

# Modified from https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py
st.title("🔎 LangChain - Chat with search")

@tool
def dummy_function(s: str) -> str:
    """I just stript input"""
    return s.strip()

#tools = [dummy_function]
tools = []

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Tell me about OpenAI real-time voice chat"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    model = ChatOpenAI(model_name="gpt-4o-mini", streaming=True)
    search = DuckDuckGoSearchRun(name="Search")
    tools.append(search)
    prompt2 = ChatPromptTemplate.from_messages(
    [
        ("system", "Respond directly without any preamble. Give numerical data and facts if possible."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)
    agent = create_tool_calling_agent(model, tools, prompt2)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        output = agent_executor.invoke({"input": prompt}, {"callbacks": [st_callback]})
        response = output["output"]
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)