# To run this code you need to install the following dependencies:
# pip install google-genai streamlit

import os

import streamlit as st
from google import genai
from google.genai import types


def generate(query: str, *, api_key: str | None = None):
    """Stream text chunks for a Google Search powered Gemini response."""
    if not query or not query.strip():
        raise ValueError("Please provide a search query.")

    resolved_api_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not resolved_api_key:
        raise ValueError(
            "Missing `GEMINI_API_KEY`. Set it in the environment or provide it in the UI."
        )

    client = genai.Client(api_key=resolved_api_key)
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=query)],
        )
    ]
    tools = [types.Tool(google_search=types.GoogleSearch())]
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""Answer without any preamble."""),
        ],
    )

    stream = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=contents,
        config=generate_content_config,
    )

    for chunk in stream:
        text_chunk = getattr(chunk, "text", None)
        if text_chunk:
            yield text_chunk


def main():
    st.set_page_config(page_title="Gemini Google Search", page_icon=":mag:")
    st.title("Gemini Google Search")
    st.caption("Search the web with Gemini's Google Search tool.")

    with st.form("google_search_form"):
        query = st.text_input(
            "Search query",
            placeholder="Latest EV news from China",
        )
        api_key = st.text_input(
            "GEMINI_API_KEY (optional)",
            type="password",
            help="Leave blank to use the GEMINI_API_KEY environment variable.",
        )
        submitted = st.form_submit_button("Search")

    results_placeholder = st.empty()

    if submitted:
        if not query.strip():
            st.warning("Please enter a search query first.")
            return

        response_buffer: list[str] = []
        try:
            with st.spinner("Searching..."):
                for chunk in generate(query, api_key=api_key.strip() or None):
                    response_buffer.append(chunk)
                    results_placeholder.markdown("".join(response_buffer))
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:  # noqa: BLE001
            st.error(f"Search failed: {exc}")


if __name__ == "__main__":
    main()
