"""Small shared utility for parsing JSON out of LLM text responses.

LLMs often wrap JSON in markdown fences or add stray whitespace; this
centralizes the cleanup so every service doesn't reimplement it.
"""
import json
import re
from typing import Any


class LLMResponseParseError(Exception):
    """Raised when an LLM response cannot be parsed as JSON."""

    def __init__(self, raw_response: str, source: Exception):
        self.raw_response = raw_response
        super().__init__(f"Could not parse JSON from LLM response: {source}\nRaw: {raw_response[:500]}")


_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def parse_json_response(raw: str) -> dict[str, Any]:
    cleaned = _FENCE_RE.sub("", raw).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        # last resort: grab the first {...} block
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        raise LLMResponseParseError(raw, exc) from exc
