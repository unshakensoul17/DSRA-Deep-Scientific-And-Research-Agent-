import os
import json
from utils import config
from datetime import datetime


class DashboardGenerator:

    def __init__(self):
        self.output_dir = config.OUTPUT_DIR

    def build_dashboard(self):
        reports = self._load_reports()

        if not reports:
            print("⚠ No reports found to generate dashboard.")
            return

        dashboard = {
            "generated_at": str(datetime.now()),
            "total_reports": len(reports),
            "topics": []
        }

        for report in reports:
            dashboard["topics"].append({
                "title": report.get("title", "Unknown"),
                "summary_snippet": report.get("summary", "").split(".")[0][:200] + "...",
                "key_findings_count": len(report.get("key_findings", [])),
                "source_count": len(report.get("cited_sources", []))
            })

        # Save JSON
        json_path = os.path.join(self.output_dir, "MASTER_DASHBOARD.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(dashboard, f, indent=4)
        print(f"📊 Dashboard JSON saved → {json_path}")

        # Save Markdown
        md_path = os.path.join(self.output_dir, "MASTER_DASHBOARD.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(self._to_markdown(dashboard))
        print(f"📄 Dashboard Markdown saved → {md_path}")


    # ----------------- FIXED: INDENTED CORRECTLY ----------------- #
    def _load_reports(self):
        files = [f for f in os.listdir(self.output_dir) if f.endswith(".json")]
        reports = []

        for file in files:
            try:
                with open(os.path.join(self.output_dir, file), "r", encoding="utf-8") as f:
                    content = f.read().strip()

                    if not content or not content.startswith("{"):
                        print(f"⚠ Skipped invalid or empty file → {file}")
                        continue

                    reports.append(json.loads(content))

            except Exception as e:
                print(f"⚠ Failed to load {file}: {e}")
                continue

        return reports
    # --------------------------------------------------------------- #


    def _to_markdown(self, dashboard):
        md = f"# 📊 DRSA Research Dashboard\nGenerated: {dashboard['generated_at']}\n\n"
        md += f"### Total Reports: **{dashboard['total_reports']}**\n\n"
        md += "| Topic | Summary | Findings | Sources |\n"
        md += "|---|---|---|---|\n"

        for t in dashboard["topics"]:
            md += f"| {t['title']} | {t['summary_snippet']} | {t['key_findings_count']} | {t['source_count']} |\n"

        return md
