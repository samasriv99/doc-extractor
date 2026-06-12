"""Document classification service.

Uses a single VisionLLMClient (per the agreed design: classification is
low-ambiguity, dual-LLM verification is reserved for extraction).
"""
from docextract.core.json_utils import parse_json_response
from docextract.core.models import ClassificationResult, DocumentType, UnsupportedDocumentError
from docextract.llm.base import VisionLLMClient
from docextract.prompts.registry import CLASSIFICATION_PROMPT


class DocumentClassifier:
    def __init__(self, llm_client: VisionLLMClient):
        self._llm = llm_client

    def classify(self, image_bytes: bytes, mime_type: str) -> ClassificationResult:
        raw = self._llm.complete(CLASSIFICATION_PROMPT, image_bytes, mime_type)
        data = parse_json_response(raw)

        label = str(data.get("label", "")).strip().lower()
        confidence = data.get("confidence")

        try:
            doc_type = DocumentType(label)
        except ValueError:
            raise UnsupportedDocumentError(detected_label=label or "unknown")

        return ClassificationResult(document_type=doc_type, confidence=confidence, raw_label=label)
