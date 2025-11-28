"""
Main Orchestrator — Multi-Topic DRSA
-----------------------------------
Handles multiple research topics, runs retriever + synthesizer + formatter
and generates reports for each topic.
"""

from core.retriever import Retriever
from core.synthesizer import Synthesizer
import os

def main():
    print("✅ DRSA Multi-Topic Agent starting...")

    # --- Get input topics ---
    user_input = input("Enter research topics (comma-separated) or path to topics.txt: ").strip()

    # Option 1: Load from file
    if os.path.exists(user_input):
        with open(user_input, "r", encoding="utf-8") as f:
            topics = [line.strip() for line in f if line.strip()]
    else:
        # Option 2: Manual comma-separated input
        topics = [t.strip() for t in user_input.split(",") if t.strip()]

    print(f"\n📚 Topics to research: {len(topics)} found → {topics}\n")

    retriever = Retriever()
    synthesizer = Synthesizer()

    for topic in topics:
        print(f"\n=== 🧠 Researching: {topic} ===")
        try:
            results = retriever.fetch_all_sources(topic)
            if not results:
                print(f"⚠️ No sources found for {topic}")
                continue

            report = synthesizer.synthesize_report(topic, results)
            if report:
                print(f"✅ Completed report for: {topic}\n")
            else:
                print(f"⚠️ Failed to synthesize {topic}\n")

        except Exception as e:
            print(f"❌ Error processing {topic}: {e}")

    print("\n🎉 All topics processed successfully!")

if __name__ == "__main__":
    main()

from core.dashboard import DashboardGenerator

# After multi-topic processing
dash = DashboardGenerator()
dash.build_dashboard()


from core.reflection import ReflectionAgent

reflect = ReflectionAgent()

# Automatically critique *ALL* generated reports
import glob
for report in glob.glob("data/outputs/*.json"):
    if "_CRITIQUE" not in report and "_IMPROVED" not in report:
        reflect.critique_report(report)
        reflect.regenerate_improved(report)

from core.memory_engine import MemoryEngine
mem = MemoryEngine()

import glob, json

# Absorb all improved or original reports
for report in glob.glob("data/outputs/*.json"):
    if "_IMPROVED" in report or "_CRITIQUE" not in report:
        with open(report, "r") as f:
            try:
                mem.absorb_report(json.load(f))
            except:
                pass

print("🧠 Knowledge updated in memory/knowledge.json")

