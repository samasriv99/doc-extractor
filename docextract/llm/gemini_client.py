"""Google Gemini vision client implementation of VisionLLMClient."""
import google.generativeai as genai
from docextract.llm.base import VisionLLMClient
from docextract.config import settings


class GeminiVisionClient(VisionLLMClient):
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self._model_name = model or settings.GEMINI_MODEL
        genai.configure(api_key=api_key or settings.GEMINI_API_KEY)
        self._model = genai.GenerativeModel(self._model_name)

    @property
    def name(self) -> str:
        return f"gemini:{self._model_name}"

    def complete(self, prompt: str, image_bytes: bytes, mime_type: str) -> str:
        response = self._model.generate_content(
            [prompt, {"mime_type": mime_type, "data": image_bytes}],
            generation_config={"temperature": 0},
        )
        return response.text or ""
