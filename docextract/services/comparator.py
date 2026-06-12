"""Compares two extraction results field-by-field after normalization, to
flag likely hallucinations / disagreements without false-positiving on
formatting differences (whitespace, case, date separators).
"""
import re
from docextract.core.models import ExtractionResult, FieldComparison, DocumentType


def _normalize(value) -> str:
    if value is None:
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"[\s\-/_.,]", "", text)  # collapse whitespace & common date/punct separators
    return text


class ResultComparator:
    def compare(
        self,
        document_type: DocumentType,
        result_a: dict,
        result_b: dict,
    ) -> ExtractionResult:
        all_fields = set(result_a) | set(result_b)
        field_comparisons: dict[str, FieldComparison] = {}
        any_disagreement = False

        for field in all_fields:
            value_a = result_a.get(field)
            value_b = result_b.get(field)
            agree = _normalize(value_a) == _normalize(value_b)
            if not agree:
                any_disagreement = True
            field_comparisons[field] = FieldComparison(
                field=field, value_a=value_a, value_b=value_b, agreement=agree
            )

        return ExtractionResult(
            document_type=document_type,
            fields=field_comparisons,
            needs_review=any_disagreement,
        )
