import os
import sys

from tavily import TavilyClient


def main() -> None:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is not set")

    query = " ".join(sys.argv[1:]) or "What are the latest developments in artificial intelligence?"
    client = TavilyClient(api_key=api_key)
    response = client.search(
        query,
        search_depth="basic",
        topic="general",
        max_results=5,
        include_answer="basic",
    )

    if answer := response.get("answer"):
        print(f"Answer:\n{answer}\n")

    print("Sources:")
    for result in response.get("results", []):
        print(f"- {result['title']}")
        print(f"  {result['url']}")
        print(f"  {result['content']}\n")


if __name__ == "__main__":
    main()