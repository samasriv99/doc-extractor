"""Core domain models, enums, and exceptions. No external deps."""
from __future__ import annotations
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    AADHAAR = "aadhaar"
    DRIVING_LICENSE = "driving_license"
    RESUME = "resume"


class UnsupportedDocumentError(Exception):
    """Raised when the document does not match a supported DocumentType."""

    def __init__(self, detected_label: str):
        self.detected_label = detected_label
        super().__init__(
            f"Unsupported document type: '{detected_label}'. "
            f"Supported types: {[t.value for t in DocumentType]}"
        )


class ClassificationResult(BaseModel):
    document_type: DocumentType
    confidence: Optional[float] = None
    raw_label: str


class FieldComparison(BaseModel):
    field: str
    value_a: Any
    value_b: Any
    agreement: bool


class ExtractionResult(BaseModel):
    document_type: DocumentType
    fields: dict[str, FieldComparison]
    needs_review: bool = Field(
        default=False, description="True if any field had disagreement between models"
    )
