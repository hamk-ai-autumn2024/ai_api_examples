import streamlit as st
from vega_datasets import data
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.line_chart(chart_data)

source = data.unemployment_across_industries()
st.area_chart(source, x="date", y="count", color="series", stack="center")

source2 = data.barley()
st.bar_chart(source2, x="variety", y="yield", color="site", horizontal=True)

df = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [60.19, 24.94],
    columns=["lat", "lon"],
)
st.map(df)