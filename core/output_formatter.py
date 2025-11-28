"""
Output Formatter Module (Enhanced)
----------------------------------
Handles saving DRSA output in JSON and Markdown format.
Now includes key findings, citations, and data validation.
"""

import os
import json
from datetime import datetime
from utils import config


class OutputFormatter:
    def __init__(self):
        # Ensure output directory exists
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    def save_output(self, report: dict):
        """
        Save synthesized report into JSON and Markdown files.
        Handles missing fields gracefully.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_title = report.get("title", "untitled_report").replace(" ", "_").lower()

        json_path = os.path.join(config.OUTPUT_DIR, f"{safe_title}_{timestamp}.json")
        md_path = os.path.join(config.OUTPUT_DIR, f"{safe_title}_{timestamp}.md")

        # 🧩 Clean up report
        structured_report = self._validate_schema(report)

        # ---- Save JSON ----
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(structured_report, f, indent=4, ensure_ascii=False)

        # ---- Save Markdown ----
        md_content = self._to_markdown(structured_report)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"\n📁 Saved JSON → {json_path}")
        print(f"📄 Saved Markdown → {md_path}")

    def _validate_schema(self, report: dict) -> dict:
        """Ensure all required fields exist based on OUTPUT_SCHEMA."""
        validated = {}
        for field, field_type in config.OUTPUT_SCHEMA.items():
            value = report.get(field)
            if value is None:
                # Provide default based on type
                if field_type == str:
                    value = "N/A"
                elif field_type == list:
                    value = []
            validated[field] = value
        return validated

    def _to_markdown(self, report: dict) -> str:
        """Convert the report dictionary into a formatted Markdown string."""
        md = f"# {report.get('title', 'Untitled Report')}\n\n"
        md += f"## 🧾 Summary\n{report.get('summary', 'No summary available.')}\n\n"

        # 🧠 Structured Research Sections
        if "sections" in report and isinstance(report["sections"], dict):
            md += "## 🧩 Research Sections\n"
            for section, content in report["sections"].items():
                title = section.replace("_", " ")
                md += f"### {title}\n{content or 'No details available.'}\n\n"

        # 🔍 Key Findings
        key_findings = report.get("key_findings", [])
        if key_findings:
            md += "## 🔍 Key Findings\n"
            for finding in key_findings:
                md += f"- {finding}\n"
            md += "\n"

        # 🌐 Cited Sources
        cited_sources = report.get("cited_sources", [])
        if cited_sources:
            md += "## 🌐 Cited Sources\n"
            for src in cited_sources:
                md += f"- {src}\n"

        return md
