# utils/pdf_utils.py
"""
PDF text extraction helper.
"""
import fitz  # PyMuPDF

def extract_text_from_pdf(path: str) -> str:
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()
