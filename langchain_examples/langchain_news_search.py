import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import load_chain
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.chains import load_summarize_chain
import os

# Streamlit app
st.subheader('Last Week In...')
open_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

# Get OpenAI API key, Serper API key, number of results, and search query
with st.sidebar:
    num_results = st.number_input("Number of Search Results", min_value=1, max_value=10)
    st.caption("*Search: Uses Serper API only, retrieves search results.*")
    st.caption("*Search & Summarize: Uses Serper & OpenAI APIs, summarizes each search result.*")
search_query = st.text_input("Search Query", label_visibility="collapsed")
col1, col2 = st.columns([1, 3])

# If the 'Search' button is clicked
if col1.button("Search"):
    # Validate inputs
    if not search_query.strip():
        st.error(f"Please provide the missing fields.")
    else:
        try:
            with st.spinner("Please wait..."):
                # Show the top X relevant news articles from the previous week using Google Serper API
                search = GoogleSerperAPIWrapper(type="news", tbs="qdr:w1", serper_api_key=serper_api_key)
                result_dict = search.results(search_query)

                if not result_dict['news']:
                    st.error(f"No search results for: {search_query}.")
                else:
                    for i, item in zip(range(num_results), result_dict['news']):
                        st.success(f"Title: {item['title']}\n\nLink: {item['link']}\n\nSnippet: {item['snippet']}")
        except Exception as e:
            st.exception(f"Exception: {e}")

# If 'Search & Summarize' button is clicked
if col2.button("Search & Summarize"):
    # Validate inputs
    if not search_query.strip():
        st.error(f"Please provide the missing fields.")
    else:
        try:
            with st.spinner("Please wait..."):
                # Show the top X relevant news articles from the previous week using Google Serper API
                search = GoogleSerperAPIWrapper(type="news", tbs="qdr:w1", serper_api_key=serper_api_key)
                result_dict = search.results(search_query)

                if not result_dict['news']:
                    st.error(f"No search results for: {search_query}.")
                else:
                    # Load URL data from the top X news search results
                    for i, item in zip(range(num_results), result_dict['news']):
                        loader = UnstructuredURLLoader(urls=[item['link']], ssl_verify=False, 
                        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                        data = loader.load()
                
                        # Initialize the ChatOpenAI module, load and run the summarize chain
                        llm = ChatOpenAI(temperature=0)
                        prompt_template = """Write a summary of the following in 100-150 words:
                            
                            {text}
        
                        """
                        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
                        chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                        summary = chain.run(data)
        
                        st.success(f"Title: {item['title']}\n\nLink: {item['link']}\n\nSummary: {summary}")
        except Exception as e:
            st.exception(f"Exception: {e}")