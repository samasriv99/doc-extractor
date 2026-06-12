"""OpenAI vision client implementation of VisionLLMClient."""
import base64
from openai import OpenAI
from docextract.llm.base import VisionLLMClient
from docextract.config import settings


class OpenAIVisionClient(VisionLLMClient):
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self._model = model or settings.OPENAI_MODEL
        self._client = OpenAI(api_key=api_key or settings.OPENAI_API_KEY)

    @property
    def name(self) -> str:
        return f"openai:{self._model}"

    def complete(self, prompt: str, image_bytes: bytes, mime_type: str) -> str:
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime_type};base64,{b64}"},
                        },
                    ],
                }
            ],
            temperature=0,
        )
        return response.choices[0].message.content or ""
