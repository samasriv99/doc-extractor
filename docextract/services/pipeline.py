"""Top-level orchestrator. Composes the smaller services; contains no LLM
or parsing logic itself (Single Responsibility = orchestration/sequencing).
"""
from docextract.core.models import ExtractionResult
from docextract.services.classifier import DocumentClassifier
from docextract.services.comparator import ResultComparator
from docextract.services.extractor import DocumentExtractor
from docextract.utils.file_utils import load_as_image


class DocumentProcessingPipeline:
    def __init__(
        self,
        classifier: DocumentClassifier,
        extractor_a: DocumentExtractor,
        extractor_b: DocumentExtractor,
        comparator: ResultComparator,
    ):
        self._classifier = classifier
        self._extractor_a = extractor_a
        self._extractor_b = extractor_b
        self._comparator = comparator

    def process(self, file_bytes: bytes, filename: str) -> ExtractionResult:
        image_bytes, mime_type = load_as_image(file_bytes, filename)

        classification = self._classifier.classify(image_bytes, mime_type)
        doc_type = classification.document_type

        result_a = self._extractor_a.extract(doc_type, image_bytes, mime_type)
        result_b = self._extractor_b.extract(doc_type, image_bytes, mime_type)

        return self._comparator.compare(doc_type, result_a, result_b)
