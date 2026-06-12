"""Abstract interface for a vision-capable LLM client.

Services depend on this abstraction (Dependency Inversion Principle), never
on a concrete provider SDK directly.
"""
from __future__ import annotations
from abc import ABC, abstractmethod


class VisionLLMClient(ABC):
    """A chat-completion client capable of accepting an image + text prompt
    and returning raw text (expected to be JSON, per prompt instructions)."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable identifier, e.g. 'gpt-4o', 'gemini-1.5-pro'."""

    @abstractmethod
    def complete(self, prompt: str, image_bytes: bytes, mime_type: str) -> str:
        """Send prompt + image, return the raw text response."""
