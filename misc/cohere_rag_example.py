import os

import cohere


MODEL = os.getenv("COHERE_MODEL", "command-a-plus-05-2026")


def main() -> None:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("COHERE_API_KEY is not set")

    client = cohere.ClientV2(api_key=api_key)

    documents = [
        cohere.Document(
            data={
                "title": "Tall penguins",
                "snippet": "Emperor penguins are the tallest.",
            }
        ),
        cohere.Document(
            data={
                "title": "Penguin habitats",
                "snippet": "Emperor penguins only live in Antarctica.",
            }
        ),
        cohere.Document(
            data={
                "title": "What are animals?",
                "snippet": "Animals are different from plants.",
            }
        ),
    ]

    message = "Where do the tallest penguins live?"
    response = client.chat(
        model=MODEL,
        messages=[cohere.UserChatMessageV2(content=message)],
        documents=documents,
    )

    content = response.message.content or []
    for item in content:
        if hasattr(item, "text"):
            print(item.text, end="")
    print()

    print("\nCitations:")
    for citation in response.message.citations or []:
        print(citation)


if __name__ == "__main__":
    main()
