import streamlit as st
import pandas as pd
from openai import OpenAI
from pydantic import BaseModel
import json

class Athlete(BaseModel):
    last_name: str
    first_name: str
    nationality: str
    record_time: float

class AthleteFormat(BaseModel):
    athletes: list[Athlete]

client = OpenAI()  # use the API key from the OPENAI_API_KEY environment variable

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        # this is the system prompt
        {"role": "system", "content": "Answer directly without any preamble. Respond in JSON format."},
        {"role": "user", "content": "List TOP10 fastest 100 meter sprinters: last name, first name, nationality, record time."},
    ],
    temperature=0.1,
    max_tokens=500,
    response_format= AthleteFormat,
)
json_text = completion.choices[0].message.content

print(type(json_text))
if json_text:
    json_full_data = json.loads(json_text)
    json_data = json_full_data["athletes"]
    st.write(json_data)
# json_data is a JSON string
# json_data = '''[
#     {"name": "John", "age": 30, "city": "New York"},
#     {"name": "Mary", "age": 25, "city": "Los Angeles"},
#     {"name": "Peter", "age": 35, "city": "Chicago"}]'''
    df = pd.read_json(json_data)  # read JSON data into a DataFrame
    edited_df = st.data_editor(df) # dataframe, which can be edited

