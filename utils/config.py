import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# API keys from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Directories
DATA_DIR = "data"
OUTPUT_DIR = os.path.join(DATA_DIR, "outputs")

# Output schema
OUTPUT_SCHEMA = {
    "title": str,
    "summary": str,
    "key_findings": list,
    "cited_sources": list,
}
