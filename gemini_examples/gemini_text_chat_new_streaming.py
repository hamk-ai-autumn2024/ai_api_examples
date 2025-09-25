import os
from typing import List
from google.genai import Client, types

def main() -> None:
    client = Client(api_key=os.getenv("GEMINI_API_KEY"))

    system_prompt = (
        "You are a concise, friendly assistant taking part in a text-based chat. "
        "Always reference prior context when responding."
    )
    history: List[types.Content] = []

    print("Type your message (empty line, 'exit', or 'quit' to leave).\n")

    while True:
        try:
            user_input = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting chat.")
            break

        if user_input.lower() in {"", "exit", "quit"}:
            print("Exiting chat.")
            break

        history.append(
            types.Content(role="user", parts=[types.Part.from_text(text=user_input)])
        )

        stream = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=history,
            config=types.GenerateContentConfig(
                temperature=1.5,
                system_instruction=system_prompt,
            ),
        )

        reply_chunks: List[str] = []
        print("Assistant: ", end="", flush=True)
        for chunk in stream:
            chunk_text = getattr(chunk, "text", None)
            if not chunk_text and getattr(chunk, "candidates", None):
                texts: List[str] = []
                for candidate in chunk.candidates:
                    content = getattr(candidate, "content", None)
                    if not content:
                        continue
                    for part in getattr(content, "parts", []) or []:
                        part_text = getattr(part, "text", None)
                        if part_text:
                            texts.append(part_text)
                chunk_text = "".join(texts)

            if chunk_text:
                print(chunk_text, end="", flush=True)
                reply_chunks.append(chunk_text)

        print("\n")

        reply = "".join(reply_chunks).strip()
        if not reply:
            print("[No text response returned]\n")
            continue

        history.append(
            types.Content(role="model", parts=[types.Part.from_text(text=reply)])
        )


if __name__ == "__main__":
    main()