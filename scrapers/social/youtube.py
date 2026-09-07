import re
from typing import List, Dict, Any, Optional

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None

from config.schemas import create_standard_lead
from core.base_scraper import BaseScraper
from lead_verifier import is_email_deliverable

class YouTubeScraper(BaseScraper):
    """Scrapes YouTube channels, media production agencies, and verified business emails."""

    def __init__(self, headless: Optional[bool] = None):
        super().__init__(name="YouTube", lead_source="YouTube", headless=headless)

    def scrape(
        self,
        keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        max_results: int = 30
    ) -> List[Dict[str, Any]]:
        leads = []
        target_locations = locations or ["Australia", "India"]
        target_keywords = keywords or ["software development tutorial", "media production agency", "odoo partner"]

        self.logger.info(f"Scraping live YouTube channel business leads for {target_locations}...")

        if not DDGS:
            self.logger.warning("DDGS module not available. Skipping YouTube query.")
            return leads

        email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

        try:
            with DDGS() as ddgs:
                for loc in target_locations:
                    for kw in target_keywords:
                        if len(leads) >= max_results:
                            break
                        query = f'site:youtube.com "{kw}" "{loc}" email OR "business inquiries"'
                        try:
                            for res in ddgs.text(query, max_results=5):
                                if len(leads) >= max_results:
                                    break
                                title = res.get("title", "")
                                body = res.get("body", "")
                                link = res.get("href", "")
                                combined = f"{title} {body}"

                                found_emails = email_regex.findall(combined)
                                valid_email = None
                                for em in found_emails:
                                    ok, clean_em, _ = is_email_deliverable(em)
                                    if ok:
                                        valid_email = clean_em
                                        break

                                if valid_email:
                                    comp_name = title.split("-")[0].split("YouTube")[0].strip()
                                    leads.append(create_standard_lead(
                                        company_name=comp_name or f"{kw.title()} Channel",
                                        lead_source=self.lead_source,
                                        source_url=link,
                                        social_url=link,
                                        email=valid_email,
                                        city=loc,
                                        country=loc,
                                        industry="Media & Technology",
                                        description=body[:200]
                                    ))
                        except Exception as e:
                            self.logger.warning(f"Error querying DDG for YouTube: {e}")
        except Exception as e:
            self.logger.warning(f"YouTube search error: {e}")

        return leads
