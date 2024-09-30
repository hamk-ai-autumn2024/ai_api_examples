import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import json

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

prompt = """List TOP10 fastest 200 m sprinters in the world in JSON format.
Use this JSON schema:

Athlete = {'last_name': str, 'first_name': str, 'nationality': str, 'record_time': float}
Return: Array[Athelete]"""

model = genai.GenerativeModel('gemini-1.5-flash',
                              generation_config={"response_mime_type": "application/json"})
result = model.generate_content(prompt)

if result:
    json_data = json.loads(result.text)
    for item in json_data:
        
        i["record_time"] = round(i["record_time"], 2)
    #json_data = json.loads(result)
    st.write(json_data)
# json_data is a JSON string
# json_data = '''[
#     {"name": "John", "age": 30, "city": "New York"},
#     {"name": "Mary", "age": 25, "city": "Los Angeles"},
#     {"name": "Peter", "age": 35, "city": "Chicago"}]'''
    df = pd.read_json(json_data)  # read JSON data into a DataFrame
    edited_df = st.data_editor(df) # dataframe, which can be edited

