import streamlit as st
import pandas as pd

# json_data is a JSON string
json_data = '''[
    {"name": "John", "age": 30, "city": "New York"},
    {"name": "Mary", "age": 25, "city": "Los Angeles"},
    {"name": "Peter", "age": 35, "city": "Chicago"}]'''
df = pd.read_json(json_data)  # read JSON data into a DataFrame
edited_df = st.data_editor(df) # dataframe, which can be edited

