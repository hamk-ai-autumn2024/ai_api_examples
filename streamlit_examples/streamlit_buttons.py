import streamlit as st
import pandas as pd
import numpy as np

def generate_large_df():
    return pd.DataFrame(
        np.random.randn(1000, 2),
        columns=['a', 'b'])

@st.cache_data
def convert_df_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

csv = convert_df_to_csv(generate_large_df())
st.button("Reset", type="primary")
if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="large_df.csv",
    mime="text/csv",
)

with st.form(key="my_form"):
    # inside the form
    sentiment_mapping = ["one", "two", "three", "four", "five"]
    selected = st.feedback("stars")
    if selected is not None:
        st.markdown(f"You selected {sentiment_mapping[selected]} star{'s' if selected != 0 else ''}.")

    import streamlit as st

    sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
    selected = st.feedback("thumbs")
    if selected is not None:
        st.markdown(f"You selected: {sentiment_mapping[selected]}")

    agree = st.checkbox("I agree")

    if agree:
        st.write("Great!")

    gender = st.radio("What is your gender?", ["male", "female", "other"])
    if gender:
        st.write(f"You are: {gender}.")

    country = st.selectbox(
        "What is your country?",
        ("Finland", "Sweden", "Bangladesh", "India", "Pakistan", "China", "USA"),
    )
    if country:
        st.write(f"You are from {country}.")

    age = st.slider("How old are you?", 0, 130, 25)
    if age:
        st.write(f"You are {age} years old")

    height = st.number_input("How tall are you cm?", min_value=0, max_value=300, value=None, placeholder="your height in cm")
    if height:
        st.write(f"You are {height} cm tall.")  

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("Form submitted")
