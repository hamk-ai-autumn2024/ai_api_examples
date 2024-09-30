import streamlit as st
import pandas as pd
import numpy as np

random_df = pd.DataFrame(np.random.randn(8, 6), columns=("col %d" % i for i in range(6)))
st.dataframe(random_df)  # Display a dataframe as an interactive table.

df_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
pd_df = pd.DataFrame(df_list, columns=["col1", "col2", "col3"])
st.table(pd_df)  # Display a dataframe as a static table.
# st.table(random_df2)  # view as a static table

df = pd.DataFrame(
    [
        {"film": "The Godfather", "rating": 4, "color_film": True},
        {"film": "Aliens", "rating": 5, "color_film": True},
        {"film": "Die Hard", "rating": 5, "color_film": True},
        {"film": "The Elephant Man", "rating": 3, "color_film": False},        
   ]
)
# The data editor widget allows you to edit dataframes and many other data structures in a table-like UI.
edited_df = st.data_editor(df) # dataframe, which can be edited

favorite_film = edited_df.loc[edited_df["rating"].idxmax()]["film"]
st.markdown(f"Your favorite film is **{favorite_film}** 🎈")


