import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

st.title("OpenAI Langchain Chat")

def generate_response(input_text):
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)
    parser = StrOutputParser()
    messages = [
        SystemMessage(content="Respond directly without any preamble."),
        HumanMessage(content=input_text),
    ]
    result = model.invoke(messages)
    parser.invoke(result)
    response = result.content
    #print(response)
    st.info(response)

with st.form("my_form"):
    text = st.text_area("Enter text:", "List 3 Python libraries for LLMs.")
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)