import streamlit as st

st.title("This is Main Title")
st.header("This is a header")
st.subheader("This is a subheader")
st.text("""Preformatted fixed-width text.""")
code = '''import streamlit as st
st.title("This is Main Title")'''
st.code(code, language='python')
st.latex(r"d = \sqrt{x^2+y^2+z^2}")
st.markdown("""This is a _markdown_ text, with HTML
<h1 style='color:red'>HTML</h1>""", unsafe_allow_html=True)
st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", caption="Streamlit logo", use_container_width=True)
st.image("petri.jpg", caption="Petri Kuittinen", use_container_width=True)
# interesting video to watch
st.video("https://www.youtube.com/watch?v=JwSS70SZdyM") # YouTube video: Build 12 Data Science Apps with Python and Streamlit
st.divider()  # similar to <hr> in HTML
st.write("This also allows _markdown_ **text** and latex $y = x^2$")
