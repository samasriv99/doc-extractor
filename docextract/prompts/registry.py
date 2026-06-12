"""Prompt templates. Kept separate from LLM/service logic (SRP)."""
from docextract.core.models import DocumentType
from docextract.core.schemas import SCHEMA_REGISTRY

CLASSIFICATION_PROMPT = """You are a document classifier for Indian documents.
Look at the attached image and classify it as exactly ONE of:
- aadhaar
- driving_license
- resume
- other

Respond with ONLY a JSON object: {"label": "<one of the above>", "confidence": <0-1 float>}
If the document does not clearly match aadhaar, driving_license, or resume, respond with "other".
"""


def extraction_prompt(document_type: DocumentType) -> str:
    schema = SCHEMA_REGISTRY[document_type]
    field_names = list(schema.model_fields.keys())
    return (
        f"You are an information extraction system for an Indian {document_type.value.replace('_', ' ')} document.\n"
        f"Extract the following fields from the attached image: {field_names}.\n"
        "Rules:\n"
        "- If a field is not present or not legible, set it to null.\n"
        "- Return dates in DD/MM/YYYY format where possible.\n"
        "- Respond with ONLY a single JSON object using exactly these keys, no extra commentary, "
        "no markdown code fences."
    )
