# api_server.py
"""
DRSA FastAPI Server + Minimal Web UI
------------------------------------
Endpoints:
 - GET  /           → HTML UI
 - POST /research   → run DRSA pipeline, return JSON + PDF path
 - GET  /download   → serve PDF
 - GET  /dashboard  → return MASTER_DASHBOARD.json (if exists)
"""

import os
import json
from typing import Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

from core.retriever import Retriever
from core.synthesizer import Synthesizer
from core.dashboard import DashboardGenerator
from core.pdf_generator import PDFGenerator
from utils import config


app = FastAPI(title="DRSA Research API")

# Templates directory for simple UI
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Optional: static for future CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")


class ResearchRequest(BaseModel):
    topic: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Simple HTML UI:
     - text box to enter topic
     - button to run research
     - area to display summary + key findings + copyable report text
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "report": None,
            "pdf_path": None,
        },
    )


@app.post("/run", response_class=HTMLResponse)
async def run_from_form(
    request: Request,
    topic: str = Form(...)
):
    retriever = Retriever()
    synthesizer = Synthesizer()
    pdf_gen = PDFGenerator()

    sources = retriever.fetch_all_sources(topic)
    if not sources:
        raise HTTPException(status_code=404, detail="No sources found.")

    report = synthesizer.synthesize_report(topic, sources)
    if not report:
        raise HTTPException(status_code=500, detail="Synthesis failed.")

    pdf_path = pdf_gen.generate_pdf(report)

    # Build copyable block (Markdown-like)
    copy_block_lines = [f"# {report.get('title','')}", "", "## Summary", report.get("summary",""), ""]
    sections = report.get("sections", {})
    if sections:
        copy_block_lines.append("## Sections")
        for sec, txt in sections.items():
            copy_block_lines.append(f"### {sec.replace('_',' ')}")
            copy_block_lines.append(txt or "")
            copy_block_lines.append("")
    kf = report.get("key_findings", [])
    if kf:
        copy_block_lines.append("## Key Findings")
        for x in kf:
            copy_block_lines.append(f"- {x}")
        copy_block_lines.append("")
    sources_list = report.get("cited_sources", [])
    if sources_list:
        copy_block_lines.append("## Cited Sources")
        for s in sources_list:
            copy_block_lines.append(f"- {s}")
    copy_block = "\n".join(copy_block_lines)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "report": report,
            "pdf_path": os.path.basename(pdf_path),
            "copy_block": copy_block,
        },
    )


@app.post("/research", response_model=dict)
async def api_research(req: ResearchRequest):
    """
    JSON API endpoint.
    POST /research { "topic": "..." }
    Returns: { report: {...}, pdf_path: "..." }
    """
    retriever = Retriever()
    synthesizer = Synthesizer()
    pdf_gen = PDFGenerator()

    sources = retriever.fetch_all_sources(req.topic)
    if not sources:
        raise HTTPException(status_code=404, detail="No sources found.")

    report = synthesizer.synthesize_report(req.topic, sources)
    if not report:
        raise HTTPException(status_code=500, detail="Synthesis failed.")

    pdf_path = pdf_gen.generate_pdf(report)

    return {
        "report": report,
        "pdf_path": os.path.basename(pdf_path),
    }


@app.get("/download")
async def download(pdf: str):
    """
    Download generated PDF by filename.
    /download?pdf=filename.pdf
    """
    full_path = os.path.join(config.OUTPUT_DIR, pdf)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(full_path, filename=pdf, media_type="application/pdf")


@app.get("/dashboard")
async def get_dashboard():
    """
    Returns MASTER_DASHBOARD.json if exists,
    otherwise triggers dashboard build.
    """
    dash = DashboardGenerator()
    dash.build_dashboard()

    dash_path = os.path.join(config.OUTPUT_DIR, "MASTER_DASHBOARD.json")
    if not os.path.exists(dash_path):
        raise HTTPException(status_code=404, detail="Dashboard not found")

    with open(dash_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return JSONResponse(data)
