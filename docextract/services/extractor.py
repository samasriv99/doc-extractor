"""Field extraction service.

A single instance is bound to one VisionLLMClient and can extract fields for
any DocumentType (the schema/prompt vary by type, the client doesn't).
"""
from docextract.core.json_utils import parse_json_response
from docextract.core.models import DocumentType
from docextract.core.schemas import SCHEMA_REGISTRY
from docextract.llm.base import VisionLLMClient
from docextract.prompts.registry import extraction_prompt


class DocumentExtractor:
    def __init__(self, llm_client: VisionLLMClient):
        self._llm = llm_client

    @property
    def source_name(self) -> str:
        return self._llm.name

    def extract(self, document_type: DocumentType, image_bytes: bytes, mime_type: str) -> dict:
        prompt = extraction_prompt(document_type)
        raw = self._llm.complete(prompt, image_bytes, mime_type)
        data = parse_json_response(raw)

        schema = SCHEMA_REGISTRY[document_type]
        # Validate + coerce against the schema; unknown keys dropped, missing -> None.
        validated = schema(**{k: data.get(k) for k in schema.model_fields})
        return validated.model_dump()
