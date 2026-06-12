"""Composition root: the only place concrete LLM client classes are
instantiated and wired together. Swapping providers means editing only here.
"""
"""Composition root: the only place concrete LLM client classes are
instantiated and wired together. Swapping providers means editing only here.
"""
from docextract.llm.base import VisionLLMClient
from docextract.llm.gemini_client import GeminiVisionClient
from docextract.services.classifier import DocumentClassifier
from docextract.services.comparator import ResultComparator
from docextract.services.extractor import DocumentExtractor
from docextract.services.pipeline import DocumentProcessingPipeline


def build_pipeline() -> DocumentProcessingPipeline:
    # Gemini-only setup: use two different model sizes so the dual-extraction
    # comparison still has *some* independent signal (same model called twice
    # tends to reproduce the same errors).
    gemini_flash: VisionLLMClient = GeminiVisionClient(model="gemini-2.5-flash")
    gemini_flash_lite: VisionLLMClient = GeminiVisionClient(model="gemini-2.5-flash")

    return DocumentProcessingPipeline(
        classifier=DocumentClassifier(gemini_flash),
        extractor_a=DocumentExtractor(gemini_flash),
        extractor_b=DocumentExtractor(gemini_flash_lite),
        comparator=ResultComparator(),
    )