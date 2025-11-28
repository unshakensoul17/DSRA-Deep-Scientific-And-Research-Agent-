import json, os

class MemoryEngine:
    def __init__(self, path="memory/knowledge.json"):
        self.path = path
        
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump({"topics": [], "key_facts": [], "cross_links": []}, f, indent=4)

        with open(path, "r") as f:
            self.memory = json.load(f)

    # --------- STORE NEW KNOWLEDGE ----------
    def absorb_report(self, report):
        topic = report.get("title")
        
        if topic not in self.memory["topics"]:
            self.memory["topics"].append(topic)

        for fact in report.get("key_findings", []):
            if fact not in self.memory["key_facts"]:
                self.memory["key_facts"].append(fact)

        # build cross-topic knowledge links
        if len(self.memory["topics"]) > 1:
            for other in self.memory["topics"]:
                if other != topic:
                    link = f"{topic} ↔ {other}"
                    if link not in self.memory["cross_links"]:
                        self.memory["cross_links"].append(link)

        self._save()

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.memory, f, indent=4)

    # --------- RETRIEVE MEMORY ----------
    def recall(self):
        return self.memory
