"""
================================================================================
🚀 CENTRALIZED GOOGLE CUSTOM SEARCH (CSE) & MULTI-ENGINE SEARCH CLIENT
================================================================================
Primary Engine: Google Custom Search JSON API (API Key + CX ID)
Secondary Engine: Google Serper API
Tertiary Fallback: DuckDuckGo Search (DDGS)
================================================================================
"""

import os
import re
import json
import requests
from typing import List, Dict, Any, Optional

from config.settings import settings
from core.logger import get_logger
from lead_verifier import is_email_deliverable

logger = get_logger("GoogleSearchClient")

class GoogleSearchClient:
    """Enterprise multi-tiered Google & Custom Search client."""

    @classmethod
    def search(
        cls,
        query: str,
        num_results: int = 10,
        target_country: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes search with prioritized engines:
        1. Official Google Custom Search JSON API (if GOOGLE_API_KEY & GOOGLE_CX_ID provided)
        2. Google Serper API (if SERPER_API_KEY provided)
        3. DuckDuckGo Search (DDGS)
        """
        results = []

        # 1. Official Google Custom Search API
        google_api_key = settings.GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY")
        
        # Route to Australia-specific CX if target country or query specifies Australia
        is_australia = (
            (target_country and target_country.lower() in ["australia", "au"]) or
            ("australia" in query.lower() or ".com.au" in query.lower())
        )
        if is_australia and settings.GOOGLE_AUSTRALIA_CX_ID:
            google_cx_id = settings.GOOGLE_AUSTRALIA_CX_ID
            logger.info("Using Australia-specific Google Custom Search Engine (CX: c1b7afab14a4b4355)")
        else:
            google_cx_id = settings.GOOGLE_CX_ID or os.getenv("GOOGLE_CX_ID") or os.getenv("CX_ID")

        if google_api_key and google_cx_id:
            try:
                logger.info(f"Querying Official Google Custom Search API ({google_cx_id}): '{query}'")
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    "key": google_api_key,
                    "cx": google_cx_id,
                    "q": query,
                    "num": min(num_results, 10)
                }
                if target_country:
                    params["gl"] = target_country.lower()[:2]

                resp = requests.get(url, params=params, timeout=12)
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get("items", [])
                    for item in items:
                        results.append({
                            "title": item.get("title", ""),
                            "link": item.get("link", ""),
                            "snippet": item.get("snippet", ""),
                            "source": "Google Custom Search API"
                        })
                    if results:
                        return results
                else:
                    logger.warning(f"Google CSE API returned status {resp.status_code}: {resp.text[:200]}")
            except Exception as e:
                logger.warning(f"Google Custom Search API error: {e}")

        # 2. Google Serper.dev API
        serper_key = settings.SERPER_API_KEY or os.getenv("SERPER_API_KEY")
        if serper_key:
            try:
                logger.info(f"Querying Google Serper API: '{query}'")
                headers = {
                    'X-API-KEY': serper_key,
                    'Content-Type': 'application/json'
                }
                payload = json.dumps({"q": query, "num": num_results})
                resp = requests.post("https://google.serper.dev/search", headers=headers, data=payload, timeout=12)
                if resp.status_code == 200:
                    data = resp.json()
                    for item in data.get("organic", []):
                        results.append({
                            "title": item.get("title", ""),
                            "link": item.get("link", ""),
                            "snippet": item.get("snippet", ""),
                            "source": "Google Serper API"
                        })
                    if results:
                        return results
            except Exception as e:
                logger.warning(f"Google Serper API error: {e}")

        # 3. DuckDuckGo Fallback Engine
        try:
            try:
                from ddgs import DDGS
            except ImportError:
                from duckduckgo_search import DDGS

            logger.info(f"Querying fallback search engine for: '{query}'")
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=num_results):
                    results.append({
                        "title": r.get("title", ""),
                        "link": r.get("href", ""),
                        "snippet": r.get("body", ""),
                        "source": "DDGS Fallback"
                    })
        except Exception as e:
            logger.warning(f"Fallback search engine error: {e}")

        return results

    @classmethod
    def search_and_extract_emails(
        cls,
        query: str,
        num_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Executes Google search and extracts 100% deliverable, zero-bounce emails and URLs.
        """
        raw_items = cls.search(query, num_results=num_results)
        email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

        extracted_leads = []
        for item in raw_items:
            combined_text = f"{item['title']} {item['snippet']}"
            found_emails = email_regex.findall(combined_text)

            valid_email = None
            for em in found_emails:
                ok, clean_em, _ = is_email_deliverable(em)
                if ok:
                    valid_email = clean_em
                    break

            if valid_email:
                extracted_leads.append({
                    "title": item["title"],
                    "link": item["link"],
                    "snippet": item["snippet"],
                    "verified_email": valid_email,
                    "source": item["source"]
                })

        return extracted_leads
