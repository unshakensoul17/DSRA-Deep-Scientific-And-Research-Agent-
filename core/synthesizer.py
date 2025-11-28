from openai import OpenAI
from utils import config
from core.output_formatter import OutputFormatter
import json, re, time


class Synthesizer:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.formatter = OutputFormatter()


    def synthesize_report(self, topic: str, sources: list):
        print("\n🤖 Generating Full-Length Research Report...")

        context = "\n\n".join([f"{s['title']} — {s['snippet']}" for s in sources[:10]]) or "No available data."

        PROMPT = f"""
Write a detailed academic research report on the topic:
**{topic}**

Use retrieved sources as reference context only.

### Output Rules
⚠ Must return STRICT JSON — no markdown, no code fences.
⚠ Summary + each section must be **complete paragraphs** (minimum 120 words).
⚠ No sentence may end mid-word or mid-sentence.
⚠ At least 4 Key Findings, each a full sentence.
⚠ At least 3 references.

### JSON Format to Output Exactly:

{{
 "title": "{topic}",
 "summary": "(120+ words, complete paragraph)",
 "sections": {{
     "Background": "(120+ words, full paragraph)",
     "Current_Challenges": "(120+ words, full paragraph)",
     "Recent_Advancements": "(120+ words, full paragraph)",
     "Future_Directions": "(120+ words, full paragraph)"
 }},
 "key_findings": ["Complete sentence 1", "Complete sentence 2", ...],
 "cited_sources": ["url1","url2","url3"]
}}
"""

        def generate():
            resp = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": PROMPT}],
                temperature=0.38
            )
            out = resp.choices[0].message.content.strip()
            out = re.sub(r"```json|```", "", out).strip()
            return out


        raw = generate()

        # 🔄 AUTO-CORRECTION LOOP
        while True:
            try:
                data = json.loads(raw)

                def incomplete(t):
                    return not t.endswith(".") or len(t.split()) < 110

                if (
                    incomplete(data["summary"]) or
                    any(incomplete(s) for s in data["sections"].values())
                ):
                    print("⚠ Incomplete report detected — regenerating...")
                    time.sleep(1.5)
                    raw = generate()
                    continue

                break  # success

            except:
                print("⚠ JSON invalid — regenerating...")
                time.sleep(1.5)
                raw = generate()


        self.formatter.save_output(data)
        print("\n✅ FULL RESEARCH REPORT GENERATED (No more cuts!)\n")
        return data
