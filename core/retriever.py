"""
Advanced Retriever Module (Phase 3 Upgrade)
------------------------------------------
Integrates 4 research sources:
 ▫ Google Search (general web pages)
 ▫ Wikipedia (overview / summaries)
 ▫ arXiv API (research papers)
 ▫ Semantic Scholar API (citations, metadata)

This makes DRSA academic-grade instead of surface search.
"""

import requests
import time
from utils import config


class Retriever:

    def __init__(self):
        self.google_api_key = config.GOOGLE_API_KEY
        self.google_cx = config.GOOGLE_CX
        self.semantic_scholar_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        self.arxiv_url = "http://export.arxiv.org/api/query?search_query="


    # =========================================================
    def fetch_all_sources(self, query: str) -> list:
        """MAIN PIPELINE : Fetch results from all 4 sources"""

        print(f"\n🔍 Fetching research data for: {query} ...")
        results = []

        results += self._fetch_from_google(query)
        results += self._fetch_from_wikipedia(query)
        results += self._fetch_from_arxiv(query)
        results += self._fetch_from_semantic_scholar(query)

        # 🔥 Remove duplicates by link/title
        unique = {
            f"{item.get('title')}{item.get('link')}": item
            for item in results
            if item.get("title") and item.get("snippet")
        }

        cleaned = list(unique.values())
        print(f"📚 Total academic quality sources → {len(cleaned)}")
        return cleaned


    # =========================================================
    def _fetch_from_google(self, query: str) -> list:
        """🔹 Standard Web Search"""
        if not self.google_api_key or not self.google_cx:
            print("⚠ Google API disabled → Skipping.")
            return []

        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.google_api_key}&cx={self.google_cx}"
        try:
            data = requests.get(url).json().get("items", [])
            return [{
                "title": i.get("title", ""),
                "link": i.get("link", ""),
                "snippet": i.get("snippet", ""),
                "source_type": "Google"
            } for i in data]
        except Exception as e:
            print("❌ Google fetch error:", e)
            return []


    # =========================================================
    def _fetch_from_wikipedia(self, query: str) -> list:
        """🔹 Fast topic summary"""
        try:
            q = query.replace(" ", "_")
            data = requests.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"
            ).json()

            if "title" not in data:
                return []

            return [{
                "title": data.get("title", ""),
                "link": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                "snippet": data.get("extract", ""),
                "source_type": "Wikipedia"
            }]
        except:
            return []


    # =========================================================
    def _fetch_from_arxiv(self, query: str) -> list:
        """🔹 Research Paper Abstracts from arXiv"""
        try:
            url = f"{self.arxiv_url}{query}&max_results=6"
            text = requests.get(url).text

            # Rough extraction — good enough for summarization pipeline
            papers = text.split("<entry>")[1:]
            results = []

            for p in papers:
                title = self._extract(p, "title")
                summary = self._extract(p, "summary")
                link = self._extract(p, "id")

                results.append({
                    "title": title.strip(),
                    "link": link.strip(),
                    "snippet": summary.strip(),
                    "source_type": "arXiv"
                })

            return results

        except Exception as e:
            print("⚠ arXiv fetch error:", e)
            return []


    def _extract(self, text, tag):
        """🧩 Small XML helper for arXiv"""
        try:
            return text.split(f"<{tag}>")[1].split(f"</{tag}>")[0]
        except:
            return "N/A"


    # =========================================================
    def _fetch_from_semantic_scholar(self, query: str) -> list:
        """🔹 Academic Search with Citation Metadata"""

        try:
            params = {
                "query": query,
                "limit": 6,
                "fields": "title,abstract,year,url,fieldsOfStudy,authors"
            }

            res = requests.get(self.semantic_scholar_url, params=params).json()
            papers = res.get("data", [])

            return [{
                "title": p.get("title", ""),
                "link": p.get("url", ""),
                "snippet": (p.get("abstract") or "")[:800],
                "year": p.get("year"),
                "authors": [a.get("name") for a in p.get("authors", [])],
                "source_type": "SemanticScholar"
            } for p in papers]

        except Exception as e:
            print("⚠ SemanticScholar fetch error:", e)
            return []
