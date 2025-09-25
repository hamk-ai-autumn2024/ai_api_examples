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

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=history,
            config=types.GenerateContentConfig(
                temperature=1.5,
                system_instruction=system_prompt,
            ),
        )

        reply = (response.text or "").strip()
        if not reply:
            print("Assistant: [No text response returned]\n")
            continue
        print(f"{reply}\n")

        history.append(
            types.Content(role="model", parts=[types.Part.from_text(text=reply)])
        )


if __name__ == "__main__":
    main()