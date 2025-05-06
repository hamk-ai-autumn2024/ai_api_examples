import streamlit as st
import validators
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader, WebBaseLoader

# You also need to install the following packages: validators, unstructured, streamlit, langchain, langchain_openai, langchain_community
# and  youtube-transcript-api and pytube
# YouTube summarization seems to be broken in the latest version of langchain_community, so we are using the YoutubeLoader from langchain_community.document_loaders

# Streamlit app
st.subheader('Summarize URL or YouTube Video')
url = st.text_input("URL", label_visibility="collapsed")

# If 'Summarize' button is clicked
if st.button("Summarize"):
    # Validate inputs
    if not url.strip():
        st.error("Please provide the missing fields.")
    elif not validators.url(url):
        st.error("Please enter a valid URL.")
    else:
        try:
            with st.spinner("Please wait..."):
                # Load URL data
                if "youtube.com" in url:
                    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[url], ssl_verify=False, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                data = loader.load()

                # Initialize the ChatOpenAI module, load and run the summarize chain
                llm = ChatOpenAI(temperature=0.3, model="gpt-4o-mini")

                # Define prompt
                prompt = ChatPromptTemplate.from_messages(
                    [("system", "Write a concise summary of the following:\\n\\n{context}")]
                )
                # Instantiate chain
                chain = create_stuff_documents_chain(llm, prompt)
                # Invoke chain
                summary = chain.invoke({"context": data})

                st.success(summary)
        except Exception as e:
            st.exception(f"Exception: {e}")
    