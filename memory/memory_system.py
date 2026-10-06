"""Simple LLM-driven user memory stored in a markdown file (no regular expressions)."""

import json
from pathlib import Path

from openai import OpenAI

DEFAULT_MODEL = "gpt-6-luna"
DEFAULT_PATH = "memory.md"

FIELDS = {
    "name": "Name",
    "age": "Age",
    "address": "Address",
    "country": "Country",
    "email": "Email",
    "phone_number": "Phone number",
    "interests": "Interests",
    "latest_chat_topic": "Latest chat topic",
}

_LABEL_TO_KEY = {label: key for key, label in FIELDS.items()}

_RULES = """Allowed fields: {fields}.

NEVER store:
- GDPR special-category data: racial/ethnic origin, political opinions, religious or philosophical beliefs,
  trade union membership, genetic or biometric data, health data, sex life or sexual orientation.
- Financial data: credit/debit card numbers, bank account numbers/IBANs, crypto wallets, etc.
- Secrets: passwords, PIN codes, API keys, tokens, authorization keys, etc.
If a value falls into one of these categories, ignore it. Do not store interests that reveal such data
(for example a medical condition, religion or political party)."""

_EXTRACT_PROMPT = """You maintain a user's profile memory.
You get the current memory and the latest user message. Decide which allowed fields must change.

{rules}

Instructions:
- Only use facts the user stated about themselves in the message. Never guess.
- "interests": return the full updated comma-separated list (merge existing and new interests).
- "latest_chat_topic": always set a short phrase (max 8 words) describing what the message is about,
  unless the message contains nothing meaningful.
- To remove a field the user asked to forget, list it in "delete".
- Return JSON only: {{"updates": {{"field": "value"}}, "delete": ["field"]}}

Current memory:
{memory}"""

_RETRIEVE_PROMPT = """You retrieve facts from a user's profile memory.
Given the memory and a user message, return only the facts that help to answer or personalise the reply.
Return a short plain-text list, one fact per line. If nothing is relevant return exactly: NONE

Memory:
{memory}"""


class MemorySystem:
    def __init__(self, client: OpenAI | None = None, model: str = DEFAULT_MODEL, path: str = DEFAULT_PATH):
        self.client = client or OpenAI()
        self.model = model
        self.path = Path(path)

    # ---- storage -------------------------------------------------------
    def load(self) -> dict[str, str]:
        if not self.path.exists():
            return {}
        data: dict[str, str] = {}
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("- **"):
                continue
            label, sep, value = line.removeprefix("- **").partition("**:")
            key = _LABEL_TO_KEY.get(label.strip())
            if sep and key and value.strip():
                data[key] = value.strip()
        return data

    def save(self, data: dict[str, str]) -> None:
        lines = ["# User Memory", ""]
        for key, label in FIELDS.items():
            if data.get(key):
                lines.append(f"- **{label}**: {data[key]}")
        self.path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def clear(self) -> None:
        self.path.unlink(missing_ok=True)

    def as_text(self) -> str:
        data = self.load()
        return "\n".join(f"{FIELDS[k]}: {v}" for k, v in data.items())

    # ---- model-driven operations ---------------------------------------
    def _ask(self, system: str, user: str, json_mode: bool = False) -> str:
        kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            **kwargs,
        )
        return response.choices[0].message.content or ""

    def remember(self, message: str) -> dict[str, str]:
        """Let the model extract facts from a message and update the markdown file.

        Returns the fields that were changed.
        """
        data = self.load()
        system = _EXTRACT_PROMPT.format(
            rules=_RULES.format(fields=", ".join(FIELDS)),
            memory=self.as_text() or "(empty)",
        )
        try:
            result = json.loads(self._ask(system, message, json_mode=True))
        except json.JSONDecodeError:
            return {}

        changed: dict[str, str] = {}
        updates = result.get("updates") or {}
        if isinstance(updates, dict):
            for key, value in updates.items():
                if key in FIELDS and value not in (None, "") and data.get(key) != str(value):
                    data[key] = str(value).strip()
                    changed[key] = data[key]
        deletes = result.get("delete") or []
        if isinstance(deletes, list):
            for key in deletes:
                if key in data:
                    del data[key]
                    changed[key] = ""
        if changed:
            self.save(data)
        return changed

    def recall(self, message: str) -> str:
        """Let the model pick the stored facts relevant for the given message."""
        memory = self.as_text()
        if not memory:
            return ""
        answer = self._ask(_RETRIEVE_PROMPT.format(memory=memory), message).strip()
        return "" if answer.upper() == "NONE" else answer
