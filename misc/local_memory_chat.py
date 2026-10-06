from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from tavily import TavilyClient

try:
    from memory import MemoryStore
except ImportError:
    from misc.memory import MemoryStore


LM_STUDIO_BASE_URL = "http://localhost:1234/v1"
LM_STUDIO_API_KEY = "lmstudio"
MODEL = "qwen3.6-35b-a3b-crown-halo-mtp-dynamic"
MAX_TOOL_ROUNDS = 4


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current or factual information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The focused web search query.",
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    }
]


def build_system_prompt(memory_context: str) -> str:
    return f"""You are a helpful local assistant.
Use the web_search tool when the user asks about current events, live information,
recent facts, or anything you cannot answer reliably from your existing knowledge.
When you use search results, cite the source URLs in your answer.

The following memory contains only user details explicitly allowed for storage.
Use it to make the conversation more relevant, but do not infer or add personal
facts that are not present.

{memory_context}"""


def web_search(query: str, tavily_client: TavilyClient) -> dict[str, Any]:
    response = tavily_client.search(
        query=query,
        search_depth="basic",
        topic="general",
        max_results=5,
        include_answer="basic",
    )

    return {
        "answer": response.get("answer"),
        "results": [
            {
                "title": result.get("title"),
                "url": result.get("url"),
                "content": result.get("content"),
            }
            for result in response.get("results", [])
        ],
    }


def run_assistant_turn(
    client: OpenAI,
    tavily_client: TavilyClient,
    messages: list[dict[str, Any]],
) -> str:
    for _ in range(MAX_TOOL_ROUNDS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2,
        )
        assistant_message = response.choices[0].message

        if not assistant_message.tool_calls:
            return assistant_message.content or "I did not receive a response."

        messages.append(assistant_message.model_dump(exclude_none=True))
        for tool_call in assistant_message.tool_calls:
            if tool_call.function.name != "web_search":
                continue

            try:
                arguments = json.loads(tool_call.function.arguments)
                query = arguments["query"]
                if not isinstance(query, str) or not query.strip():
                    raise ValueError("query must be a non-empty string")
                result = web_search(query, tavily_client)
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                result = {"error": f"Invalid web_search arguments: {error}"}
            except Exception as error:
                result = {"error": f"Web search failed: {error}"}

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

    return "The assistant reached the web-search limit for this turn."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local LM Studio chat with safe user memory.")
    parser.add_argument(
        "--memory-file",
        type=Path,
        help="Path for memory storage. Defaults to memory.md or LOCAL_CHAT_MEMORY_FILE.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise RuntimeError("TAVILY_API_KEY is not set")

    client = OpenAI(base_url=LM_STUDIO_BASE_URL, api_key=LM_STUDIO_API_KEY)
    tavily_client = TavilyClient(api_key=tavily_api_key)
    memory = MemoryStore(args.memory_file)
    console = Console()
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": build_system_prompt(memory.context())}
    ]

    console.print(f"[bold]Local memory chat[/bold]  [dim]{MODEL}[/dim]")
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
            answer = run_assistant_turn(client, tavily_client, messages)
        except Exception as error:
            messages.pop()
            console.print(f"[red]Request failed:[/red] {error}")
            continue

        messages.append({"role": "assistant", "content": answer})
        console.print("\n[bold green]Assistant>[/bold green]")
        console.print(Markdown(answer))


if __name__ == "__main__":
    main()
