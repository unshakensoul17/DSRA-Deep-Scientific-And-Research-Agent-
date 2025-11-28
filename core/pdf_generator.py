"""
PDF Generator (Final Fix - No Cutting, No Overflow)
---------------------------------------------------
Automatically wraps text, supports long paragraphs,
clean formatting & multi-page output.
"""

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus.tables import Table
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
import os
from utils import config
from datetime import datetime


class PDFGenerator:
    def generate_pdf(self, report: dict) -> str:
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)

        filename = f"{report['title'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"
        path = os.path.join(config.OUTPUT_DIR, filename)

        styles = getSampleStyleSheet()
        body = ParagraphStyle(
            'body',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
        )

        title_style = ParagraphStyle(
            'title',
            parent=styles['Title'],
            fontSize=20,
            textColor=colors.HexColor("#1A73E8"),
            spaceAfter=15,
            alignment=TA_JUSTIFY,
        )

        doc = SimpleDocTemplate(path, pagesize=LETTER, rightMargin=40, leftMargin=40, topMargin=50, bottomMargin=50)
        content = []

        # -------- TITLE --------
        content.append(Paragraph(report["title"], title_style))
        content.append(Spacer(1, 15))

        # -------- SUMMARY --------
        content.append(Paragraph("<b>SUMMARY</b>", styles['Heading2']))
        content.append(Paragraph(report["summary"], body))
        content.append(Spacer(1, 12))

        # -------- SECTIONS --------
        for section, text in report.get("sections", {}).items():
            content.append(Paragraph(f"<b>{section.upper()}</b>", styles['Heading3']))
            content.append(Paragraph(text, body))
            content.append(Spacer(1, 10))

        # -------- FINDINGS --------
        if report.get("key_findings"):
            content.append(PageBreak())
            content.append(Paragraph("<b>KEY FINDINGS</b>", styles['Heading2']))
            for f in report["key_findings"]:
                content.append(Paragraph(f"• {f}", body))
                content.append(Spacer(1, 6))

        # -------- REFERENCES --------
        if report.get("cited_sources"):
            content.append(PageBreak())
            content.append(Paragraph("<b>REFERENCES</b>", styles['Heading2']))
            for src in report["cited_sources"]:
                content.append(Paragraph(f"- {src}", body))
                content.append(Spacer(1, 4))

        doc.build(content)
        print(f"\n📄 PDF Generated Successfully → {path}\n")
        return path
