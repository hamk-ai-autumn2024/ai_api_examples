from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

try:
    from memory import MemoryStore
except ImportError:
    from misc.memory import MemoryStore


MODEL = "gpt-6-luna"
TEMPERATURE = 0.7


def build_system_prompt(memory_context: str) -> str:
    return f"""You are a helpful assistant.
Answer clearly and accurately. Do not claim to have current information unless it
is provided in the conversation.

The following memory contains only user details explicitly allowed for storage.
Use it to make the conversation more relevant, but do not infer or add personal
facts that are not present.

{memory_context}"""


def run_assistant_turn(
    client: OpenAI,
    messages: list[dict[str, Any]],
) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        #temperature=TEMPERATURE,
    )
    return response.choices[0].message.content or "I did not receive a response."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpenAI chat with safe user memory.")
    parser.add_argument(
        "--memory-file",
        type=Path,
        help="Path for memory storage. Defaults to memory.md or LOCAL_CHAT_MEMORY_FILE.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")

    client = OpenAI()
    memory = MemoryStore(args.memory_file)
    console = Console()
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": build_system_prompt(memory.context())}
    ]

    console.print(f"[bold]OpenAI memory chat[/bold]  [dim]{MODEL}[/dim]")
    console.print(f"[dim]Memory file: {memory.path}[/dim]")
    console.print(
        "Type /help for commands, /memory to inspect saved memory, "
        "/reset to clear chat, or /quit to exit."
    )

    while True:
        try:
            user_input = console.input("\n[bold cyan]You>[/bold cyan] ")
        except (EOFError, KeyboardInterrupt):
            console.print("\nGoodbye.")
            return

        command = user_input.strip().lower()
        if not user_input.strip():
            continue
        if command in {"/quit", "/exit"}:
            console.print("Goodbye.")
            return
        if command == "/help":
            console.print(
                "[dim]/memory shows saved nuggets. /forget deletes them. "
                "/reset clears only the chat context.\n"
                "Sensitive, financial, and secret information is never saved.[/dim]"
            )
            continue
        if command == "/memory":
            console.print(Markdown(memory.context()))
            continue
        if command == "/forget":
            memory.clear()
            messages = [
                {"role": "system", "content": build_system_prompt(memory.context())}
            ]
            console.print("[dim]Saved memory deleted.[/dim]")
            continue
        if command == "/reset":
            messages = [
                {"role": "system", "content": build_system_prompt(memory.context())}
            ]
            console.print("[dim]Chat context reset. Saved memory remains available.[/dim]")
            continue

        update = memory.remember_with_model(user_input, client, MODEL)
        if update.blocked:
            console.print("[dim]Sensitive, financial, or secret content was not saved.[/dim]")
        elif update.changed_fields:
            labels = ", ".join(update.changed_fields)
            console.print(f"[dim]Memory updated: {labels}[/dim]")
        messages[0]["content"] = build_system_prompt(memory.context())

        messages.append({"role": "user", "content": user_input})
        try:
            answer = run_assistant_turn(client, messages)
        except Exception as error:
            messages.pop()
            console.print(f"[red]Request failed:[/red] {error}")
            continue

        messages.append({"role": "assistant", "content": answer})
        console.print("\n[bold green]Assistant>[/bold green]")
        console.print(Markdown(answer))


if __name__ == "__main__":
    main()
