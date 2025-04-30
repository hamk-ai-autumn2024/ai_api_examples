import streamlit as st

def reverse_string(s):
    return s[::-1]

messages = st.container()
if prompt := st.chat_input("Say something"):
    messages.chat_message("user").write(prompt)
    reversed_prompt = reverse_string(prompt)
    messages.chat_message("assistant").write(f"Reversed: {reversed_prompt}")