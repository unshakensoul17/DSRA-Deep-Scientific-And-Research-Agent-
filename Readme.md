
# 🧠 DRSA — Deep Scientific & Research Agent

📄 Automated AI-Research System | 🔍 Retrieval + Synthesis + PDF Export | 🌐 FastAPI Web App
🔗 **Live Deployment:** [https://dsra-deep-scientific-and-research-agent.onrender.com](https://dsra-deep-scientific-and-research-agent.onrender.com)

---

## Overview

**DRSA (Deep Scientific & Research Agent)** is a fully automated research intelligence pipeline designed to **search, analyze, summarize, verify, and export knowledge** on any scientific topic.

It acts as a **Mini DeepMind-like research assistant**, capable of turning raw internet data into structured research reports with:

| Module               | Function                                                       |
| -------------------- | -------------------------------------------------------------- |
| 🔎 Retriever         | Fetches research from Wikipedia, ArXiv, Semantic Scholar & Web |
| 🧠 Synthesizer       | Converts data into structured academic reports                 |
| 📄 Formatter         | Saves structured markdown, JSON & dashboard                    |
| 🧾 PDF Engine        | Generates formal research paper-style PDF reports              |
| 🌍 FastAPI Web UI    | Live browser-based interface + download support                |
| 📊 Dashboard Builder | Creates summaries of all previously generated reports          |

---

## Features

| Feature                                              | Status |
| ---------------------------------------------------- | ------ |
| Multi-Source Data Retrieval (Wiki + ArXiv + Scholar) | ✔      |
| AI-powered Research Summarization                    | ✔      |
| JSON + Markdown Report Generation                    | ✔      |
| PDF Export with Beautiful Formatting                 | ✔      |
| FastAPI Web UI + Form-based research input           | ✔      |
| REST API Endpoint (`POST /research`)                 | ✔      |
| Auto Dashboard Generator                             | ✔      |
| Deployment on Render                                 | ✔      |

📌 **You enter a research topic → DRSA performs full research → outputs verified report.**

---

## Workflow / Pipeline Architecture

```
                    ┌─────────────────────────┐
                    │        USER INPUT        │
                    └─────────────┬───────────┘
                                  │
                            (FastAPI UI)
                                  │
                                  ▼
                       🔍 Retriever Module
         ───────────────────────────────────────────
         Sources → Wikipedia / ArXiv / Scholar / Web
         ───────────────────────────────────────────
                                  │
                                  ▼
                       🧠 Synthesizer Engine
              → Creates structured research output
              → Sections, summary, insights, sources
                                  │
                                  ▼
                        📝 Output Formatter
              Saves:  JSON  +  Markdown  +  Dashboard
                                  │
                                  ▼
                       📄 PDF Generation Engine
                                  │
                                  ▼
                      🌍 Web UI + API Response
```

---

## Project Structure

```
📦 DSRA Project
│── main.py                        # Local execution entry
│── api_server.py                  # FastAPI server + Web UI
│── requirements.txt               # Python dependencies
│── README.md                      # Documentation (You are here)
│── start.sh                       # Render startup command
│
├── core/
│   ├── retriever.py               # Multi-source research fetcher
│   ├── synthesizer.py             # LLM research summarizer
│   ├── output_formatter.py        # JSON/Markdown exporter
│   ├── pdf_generator.py           # PDF report engine
│   ├── dashboard.py               # Generates MASTER_DASHBOARD
│
├── templates/
│   └── index.html                 # Web UI layout rendered on FastAPI
│
├── static/
│   └── style.css                  # UI styling & theme (editable)
│
├── utils/
│   └── config.py                  # API keys + paths + environment loader
│
└── data/outputs/                  # Saved reports + PDFs
```

---

## Local Development Setup

### 1️⃣ Clone repo & create virtual environment

```bash
git clone <YOUR_REPO_URL>
cd DSRA\ Project
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Add environment variables

Create `.env` in root:

```
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
GOOGLE_CX=your_google_cx_here
```

### 4️⃣ Run Web UI manually

```bash
uvicorn api_server:app --reload
```

---

## Deployment (Render)

✔ Already deployed at:
**🔗 [https://dsra-deep-scientific-and-research-agent.onrender.com](https://dsra-deep-scientific-and-research-agent.onrender.com)**

### Deployment Files Used

| File             | Purpose                   |
| ---------------- | ------------------------- |
| requirements.txt | Build environment         |
| start.sh         | Server startup for Render |
| api_server.py    | Web entrypoint            |

Users can now access the tool globally without installation.

---

## API Usage (Developers)

### 📌 Endpoint: Generate Research

```http
POST /research
Content-Type: application/json
{
    "topic": "Quantum Computing in Medicine"
}
```

### Response

```json
{
  "report": { ...full structured summary... },
  "pdf_path": "quantum_computing_2025.pdf"
}
```

---

## Roadmap (Upcoming Versions)

| Feature                           | Status              |
| --------------------------------- | ------------------- |
| 🧪 Claim Verification Engine      | ⏳ planned           |
| 📊 Vercel Frontend Dashboard      | ⏳ coming            |
| 🔊 Voice-driven Research Agent    | ⏳ coming            |
| 🗄 Database + Report History UI   | ⏳ coming            |
| 🚀 HuggingFace + CloudGPU Backend | 🔥 future expansion |

---

## Author

**Akash | Research Engineer & AI Developer**
📧 Contact for collaboration anytime.
email : aakashyaduwanshi0470@gmail.com

---
