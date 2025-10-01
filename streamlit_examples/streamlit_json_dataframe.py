import streamlit as st
import pandas as pd
from io import StringIO

# json_data is a JSON string
json_data = '''[
    {"name": "John", "age": 30, "city": "New York"},
    {"name": "Mary", "age": 25, "city": "Los Angeles"},
    {"name": "Peter", "age": 35, "city": "Chicago"}]'''
# Wrap literal JSON in StringIO to avoid pandas deprecation warning
df = pd.read_json(StringIO(json_data))
edited_df = st.data_editor(df) # dataframe, which can be edited
