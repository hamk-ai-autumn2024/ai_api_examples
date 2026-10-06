from __future__ import annotations

import os
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Pattern


MEMORY_FIELDS = (
    "name",
    "age",
    "country",
    "address",
    "interests",
    "last_chat_topic",
)

FIELD_LABELS = {
    "name": "Name",
    "age": "Age",
    "country": "Country",
    "address": "Address",
    "interests": "Interests",
    "last_chat_topic": "Last chat topic",
}

PROTECTED_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(
        r"\b(?:health|medical|medicine|diagnosis|disease|illness|symptom|"
        r"treatment|medication|disability|pregnant|pregnancy)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:sexual|sex life|sexuality|sexual orientation|lgbtq|gay|"
        r"lesbian|bisexual|transgender|gender identity)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:race|racial|ethnic|ethnicity|religion|religious|political|"
        r"trade union|union membership|biometric|fingerprint|facial recognition|"
        r"dna|genetic|criminal record|conviction|arrest)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:credit card|debit card|bank account|account number|routing number|"
        r"iban|swift|salary|income|financial|finance|loan|mortgage|debt|"
        r"tax return|investment|cryptocurrency|crypto wallet|wallet address)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:password|passcode|api[\s_-]?key|secret|credential|credentials|"
        r"token|access token|bearer token|auth token|private key|seed phrase|"
        r"one[-\s]?time password|otp|security code)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:ssn|social security number)\b", re.IGNORECASE),
    re.compile(r"\b(?:sk|tvly|pk)-[A-Za-z0-9_-]{8,}\b"),
)

_EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
_PHONE_PATTERN = re.compile(r"\b\+?\d[\d ()-]{7,}\d\b")
_URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)

_NAME_PATTERNS = (
    re.compile(r"\b(?:my name is|call me)\s+([^.!?,;\n]+)", re.IGNORECASE),
    re.compile(
        r"\bI(?:'m| am)\s+([A-Z][A-Za-z.'-]*(?:\s+[A-Z][A-Za-z.'-]*){0,2})\b"
    ),
)
_AGE_PATTERNS = (
    re.compile(
        r"\b(?:I just|I recently) turned\s+(\d{1,3})\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:today is|it is|it's)\s+my\s+(\d{1,3})(?:st|nd|rd|th)\s+birthday\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:I am|I'm|my age is)\s+(\d{1,3})"
        r"(?:\s+years?\s+old)?\b",
        re.IGNORECASE,
    ),
)
_COUNTRY_PATTERNS = (
    re.compile(
        r"\b(?:I live in|I'm from|I am from|my country is)\s+([^.!?,;\n]+)",
        re.IGNORECASE,
    ),
)
_ADDRESS_PATTERNS = (
    re.compile(
        r"\b(?:my address is|my home address is|I live at)\s+([^.!?\n]+)",
        re.IGNORECASE,
    ),
)
_INTEREST_PATTERNS = (
    re.compile(
        r"\b(?:my interests?(?: are| include| in)|I (?:like|love|enjoy)|"
        r"I am interested in|I'm interested in)\s+([^.!?\n]+)",
        re.IGNORECASE,
    ),
)

_EXTRACTION_PATTERNS = (
    *_NAME_PATTERNS,
    *_AGE_PATTERNS,
    *_COUNTRY_PATTERNS,
    *_ADDRESS_PATTERNS,
    *_INTEREST_PATTERNS,
)

_MODEL_EXTRACTION_PROMPT = """Extract explicit user facts from the user message.
Return one JSON object with only these keys: name, age, country, address,
interests, last_chat_topic. Use null for unknown fields.

Rules:
- Never infer facts that are not explicitly stated.
- For age, understand natural language such as "I just turned 24" or "Today is
    my 24th birthday" and return the numeric string "24".
- Return age as a number string, not a calculation or explanation.
- The application already blocks sensitive, financial, and secret content before
    this prompt is sent. Do not add any such information if it appears.
- Return JSON only, with no markdown or commentary.
"""


@dataclass(frozen=True)
class MemoryUpdate:
    changed_fields: tuple[str, ...] = ()
    blocked: bool = False


class MemoryStore:
    """Persist a small, explicitly allow-listed set of user memory fields."""

    def __init__(self, path: str | Path | None = None) -> None:
        configured_path = path or os.getenv("LOCAL_CHAT_MEMORY_FILE") or "memory.md"
        self.path = Path(configured_path)
        self._data = self._load()

    @property
    def data(self) -> dict[str, str]:
        return dict(self._data)

    def context(self) -> str:
        if not self._data:
            return "No user memory has been saved yet."

        lines = ["Saved user memory:"]
        for field in MEMORY_FIELDS:
            if field in self._data:
                lines.append(f"- {FIELD_LABELS[field]}: {self._data[field]}")
        return "\n".join(lines)

    def remember(self, user_message: str) -> MemoryUpdate:
        if not user_message.strip():
            return MemoryUpdate()

        if contains_protected_content(user_message):
            return MemoryUpdate(blocked=True)

        return self._apply_candidates(user_message, {
            **self._regex_candidates(user_message),
        })

    def remember_with_model(
        self, user_message: str, client: Any, model: str
    ) -> MemoryUpdate:
        """Use the chat model to understand natural language before saving."""
        if not user_message.strip():
            return MemoryUpdate()

        if contains_protected_content(user_message):
            return MemoryUpdate(blocked=True)

        candidates = self._regex_candidates(user_message)
        candidates.update(_extract_with_model(client, model, user_message))
        return self._apply_candidates(user_message, candidates)

    def _regex_candidates(self, user_message: str) -> dict[str, str | None]:
        return {
            "name": _extract_value(_NAME_PATTERNS, user_message),
            "age": _extract_value(_AGE_PATTERNS, user_message, split_conjunction=False),
            "country": _extract_value(_COUNTRY_PATTERNS, user_message),
            "address": _extract_value(_ADDRESS_PATTERNS, user_message, split_conjunction=False),
            "interests": _extract_value(_INTEREST_PATTERNS, user_message, split_conjunction=False),
            "last_chat_topic": _topic_from_message(user_message),
        }

    def _apply_candidates(
        self, user_message: str, candidates: dict[str, str | None]
    ) -> MemoryUpdate:
        updates: dict[str, str] = {}
        for field, value in candidates.items():
            safe_value = _safe_value(field, value)
            if safe_value and self._data.get(field) != safe_value:
                updates[field] = safe_value

        if not updates:
            return MemoryUpdate()

        self._data.update(updates)
        self.save()
        return MemoryUpdate(changed_fields=tuple(updates))

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["# User Memory", ""]
        for field in MEMORY_FIELDS:
            value = self._data.get(field)
            if value:
                lines.append(f"- {FIELD_LABELS[field]}: {value}")
        self.path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def clear(self) -> None:
        self._data.clear()
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass

    def _load(self) -> dict[str, str]:
        if not self.path.is_file():
            return {}

        try:
            content = self.path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return {}

        labels = {label.lower(): field for field, label in FIELD_LABELS.items()}
        data: dict[str, str] = {}
        for line in content.splitlines():
            match = re.match(r"^-\s+([^:]+):\s*(.+?)\s*$", line)
            if not match:
                continue
            field = labels.get(match.group(1).strip().lower())
            if field is None:
                continue
            value = _safe_value(field, match.group(2))
            if value:
                data[field] = value
        return data


def contains_protected_content(text: str) -> bool:
    return any(pattern.search(text) for pattern in PROTECTED_PATTERNS)


def _extract_with_model(client: Any, model: str, user_message: str) -> dict[str, str]:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _MODEL_EXTRACTION_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        payload = json.loads(content)
    except (AttributeError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        return {}
    except Exception:
        return {}

    if not isinstance(payload, dict):
        return {}

    return {
        field: value
        for field in MEMORY_FIELDS
        if isinstance(value := payload.get(field), (str, int, float))
    }


def _extract_value(
    patterns: tuple[Pattern[str], ...], text: str, *, split_conjunction: bool = True
) -> str | None:
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            value = match.group(1)
            if split_conjunction:
                value = re.split(r"\s+(?:and|but|because|while|when)\s+", value, maxsplit=1, flags=re.IGNORECASE)[0]
            return _clean_value(value)
    return None


def _safe_value(field: str, value: str | None) -> str | None:
    if not value:
        return None

    cleaned = _clean_value(value)
    if not cleaned or contains_protected_content(cleaned):
        return None

    if field == "age":
        try:
            age = int(cleaned)
        except ValueError:
            return None
        if not 0 <= age <= 130:
            return None
        return str(age)

    maximum_lengths = {
        "name": 80,
        "country": 80,
        "address": 240,
        "interests": 240,
        "last_chat_topic": 160,
    }
    return cleaned[: maximum_lengths[field]]


def _clean_value(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip(" \t\r\n.,;:-")


def _topic_from_message(text: str) -> str | None:
    topic = text
    for pattern in _EXTRACTION_PATTERNS:
        topic = pattern.sub(" ", topic)
    topic = _EMAIL_PATTERN.sub(" ", topic)
    topic = _PHONE_PATTERN.sub(" ", topic)
    topic = _URL_PATTERN.sub(" ", topic)
    topic = _clean_value(topic)
    if len(topic.split()) < 2:
        return None
    return topic
