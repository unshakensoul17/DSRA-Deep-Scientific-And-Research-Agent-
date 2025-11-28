"""
Reflection Module — Phase 3.3
The agent reads its own reports, critiques them, and can regenerate improved versions.
"""

from openai import OpenAI
from utils import config
import json
import os

class ReflectionAgent:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def critique_report(self, report_path):
        """Reads a JSON report → generates weaknesses & suggestions."""
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)

        prompt = f"""
You are an expert research analyst.
Evaluate this research report for quality, completeness, and depth.

Report:
{json.dumps(report, indent=2)}

Return your response in STRICT JSON:

{{
  "strengths": ["..."],
  "weaknesses": ["..."],
  "missing_points": ["..."],
  "improvement_plan": ["Step1","Step2","..."]
}}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        critique = response.choices[0].message.content

        # Save critique next to original report
        critique_path = report_path.replace(".json", "_CRITIQUE.json")
        with open(critique_path, "w", encoding="utf-8") as f:
            f.write(critique)

        print(f"📝 Critique saved → {critique_path}")
        return critique


    def regenerate_improved(self, report_path):
        """Uses weaknesses to rewrite a better final report."""
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)

        critique_file = report_path.replace(".json", "_CRITIQUE.json")
        with open(critique_file, "r", encoding="utf-8") as c:
            critique = c.read()

        prompt = f"""
You are an autonomous AI researcher.
Improve this report using the critique feedback.

Original Report:
{json.dumps(report, indent=2)}

Critique Feedback:
{critique}

Rewrite the report as HIGH-QUALITY JSON with more depth, citations, clarity and structure.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        improved = response.choices[0].message.content

        improved_path = report_path.replace(".json", "_IMPROVED.json")
        with open(improved_path, "w", encoding="utf-8") as f:
            f.write(improved)

        print(f"🔥 Improved report generated → {improved_path}")
        return improved
