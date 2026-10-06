import json
import os
from typing import Any

from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from tavily import TavilyClient


LM_STUDIO_BASE_URL = "http://localhost:1234/v1"
LM_STUDIO_API_KEY = "lmstudio"
MODEL = "qwen3.6-35b-a3b-crown-halo-mtp-dynamic"
MAX_TOOL_ROUNDS = 4

SYSTEM_PROMPT = """You are a helpful local assistant.
Use the web_search tool when the user asks about current events, live information,
recent facts, or anything you cannot answer reliably from your existing knowledge.
When you use search results, cite the source URLs in your answer."""

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
                result = web_search(query, tavily_client)
            except (KeyError, TypeError, json.JSONDecodeError) as error:
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


def main() -> None:
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise RuntimeError("TAVILY_API_KEY is not set")

    client = OpenAI(base_url=LM_STUDIO_BASE_URL, api_key=LM_STUDIO_API_KEY)
    tavily_client = TavilyClient(api_key=tavily_api_key)
    console = Console()
    messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]

    console.print(f"[bold]Local chat[/bold]  [dim]{MODEL}[/dim]")
    console.print("Type /help for commands, /reset to clear the conversation, or /quit to exit.")

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
            console.print("[dim]/reset clears chat history. /quit exits the program.[/dim]")
            continue
        if command == "/reset":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            console.print("[dim]Conversation reset.[/dim]")
            continue

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