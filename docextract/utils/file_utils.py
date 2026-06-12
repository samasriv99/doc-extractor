"""Normalizes uploaded documents (jpeg/png/pdf) into a single image suitable
for vision LLMs. Single Responsibility: input normalization only.
"""
import io
import fitz  # PyMuPDF


SUPPORTED_IMAGE_MIME = {"image/jpeg", "image/jpg", "image/png"}


class UnsupportedFileTypeError(Exception):
    def __init__(self, filename: str):
        super().__init__(f"Unsupported file type for: {filename}")


def load_as_image(file_bytes: bytes, filename: str) -> tuple[bytes, str]:
    """Returns (image_bytes, mime_type). For PDFs, renders the first page."""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return _first_page_to_png(file_bytes)
    if lower.endswith((".jpg", ".jpeg")):
        return file_bytes, "image/jpeg"
    if lower.endswith(".png"):
        return file_bytes, "image/png"
    raise UnsupportedFileTypeError(filename)


def _first_page_to_png(pdf_bytes: bytes, dpi: int = 200) -> tuple[bytes, str]:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    try:
        page = doc.load_page(0)
        zoom = dpi / 72
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        buf = io.BytesIO(pix.tobytes("png"))
        return buf.getvalue(), "image/png"
    finally:
        doc.close()
