"""Rich terminal chat that remembers user data via MemorySystem."""

from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from memory_system import DEFAULT_MODEL, FIELDS, MemorySystem

console = Console()
client = OpenAI()
memory = MemorySystem(client=client, model=DEFAULT_MODEL)

SYSTEM_PROMPT = (
    "You are a friendly assistant. Use the remembered user facts naturally when they are relevant, "
    "but do not mention the memory system unless asked."
)

HELP = "Commands: /memory show stored data, /forget delete all memory, /quit exit"


def show_memory() -> None:
    data = memory.load()
    if not data:
        console.print("[yellow]Memory is empty.[/yellow]")
        return
    console.print(Panel(Markdown("\n".join(f"- **{FIELDS[k]}**: {v}" for k, v in data.items())), title="Memory"))


def main() -> None:
    console.print(Panel(f"[bold]Memory chat[/bold] ({DEFAULT_MODEL})\n{HELP}", border_style="cyan"))
    history: list[dict[str, str]] = []

    while True:
        user_input = Prompt.ask("[bold green]You[/bold green]").strip()
        if not user_input:
            continue
        if user_input == "/quit":
            break
        if user_input == "/memory":
            show_memory()
            continue
        if user_input == "/forget":
            memory.clear()
            console.print("[yellow]Memory cleared.[/yellow]")
            continue

        try:
            with console.status("Updating memory..."):
                changed = memory.remember(user_input)
                facts = memory.recall(user_input)
            if changed:
                summary = ", ".join(FIELDS[k] for k in changed)
                console.print(f"[dim]Memory updated: {summary}[/dim]")

            system = SYSTEM_PROMPT + (f"\n\nKnown facts about the user:\n{facts}" if facts else "")
            history.append({"role": "user", "content": user_input})
            with console.status("Thinking..."):
                response = client.chat.completions.create(
                    model=DEFAULT_MODEL,
                    messages=[{"role": "system", "content": system}, *history],
                )
            reply = response.choices[0].message.content or ""
        except Exception as exc:
            if history and history[-1]["role"] == "user":
                history.pop()
            console.print(f"[red]Error: {exc}[/red]")
            continue

        history.append({"role": "assistant", "content": reply})
        console.print(Panel(Markdown(reply), title="Assistant", border_style="blue"))


if __name__ == "__main__":
    main()
