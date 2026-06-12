"""FastAPI app exposing /api/extract, with a Gradio UI mounted at /.

The Gradio UI itself calls the FastAPI endpoint via HTTP, keeping the UI
layer fully decoupled from pipeline internals.
"""
import io
import requests
import gradio as gr
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from docextract.api.dependencies import build_pipeline
from docextract.core.models import UnsupportedDocumentError
from docextract.core.json_utils import LLMResponseParseError

app = FastAPI(title="Indian Document Extraction API")
_pipeline = build_pipeline()


@app.post("/api/extract")
async def extract_document(file: UploadFile = File(...)):
    file_bytes = await file.read()
    try:
        result = _pipeline.process(file_bytes, file.filename)
    except UnsupportedDocumentError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except LLMResponseParseError as exc:
        raise HTTPException(status_code=502, detail=f"LLM returned unparseable output: {exc}") from exc
    return JSONResponse(content=result.model_dump())


# --- Gradio UI -------------------------------------------------------------

def _call_extract_api(file_path: str) -> tuple[str, str]:
    """Calls our own FastAPI endpoint. Returns (doc_type, formatted_table_md)."""
    if file_path is None:
        return "", "Please upload a document."

    with open(file_path, "rb") as f:
        files = {"file": (file_path.split("/")[-1], f)}
        try:
            response = requests.post("http://127.0.0.1:8000/api/extract", files=files, timeout=120)
        except requests.RequestException as exc:
            return "", f"Request failed: {exc}"

    if response.status_code != 200:
        try:
            detail = response.json().get("detail")
        except ValueError:
            detail = response.text[:1000]
        return "", f"Error ({response.status_code}): {detail}"

    data = response.json()
    doc_type = data["document_type"]

    rows = ["| Field | Model A | Model B | Agreement |", "|---|---|---|---|"]
    for field, comp in data["fields"].items():
        flag = "✅" if comp["agreement"] else "⚠️ MISMATCH"
        rows.append(f"| {field} | {comp['value_a']} | {comp['value_b']} | {flag} |")

    if data["needs_review"]:
        rows.append("")
        rows.append("**⚠️ One or more fields disagree between models — manual review recommended.**")

    return doc_type, "\n".join(rows)


with gr.Blocks(title="Indian Document Extractor") as demo:
    gr.Markdown("## Indian Document Extractor\nUpload an Aadhaar, Driving License, or Resume (JPEG/PDF).")
    file_input = gr.File(label="Document", file_types=[".jpg", ".jpeg", ".png", ".pdf"], type="filepath")
    submit_btn = gr.Button("Extract")
    doc_type_output = gr.Textbox(label="Detected Document Type")
    results_output = gr.Markdown(label="Extracted Fields")

    submit_btn.click(fn=_call_extract_api, inputs=file_input, outputs=[doc_type_output, results_output])


app = gr.mount_gradio_app(app, demo, path="/")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
