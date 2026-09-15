import re
from typing import List, Dict, Any, Optional
from config.schemas import create_standard_lead
from core.base_scraper import BaseScraper
from core.google_search import GoogleSearchClient

class SerperSocialScraper(BaseScraper):
    """Executes high-intent Google & CSE Dork searches for business leads."""

    def __init__(self, headless: Optional[bool] = None):
        super().__init__(name="SerperSocial", lead_source="Google Custom Search & Dorking", headless=headless)

    def scrape(
        self,
        keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        leads = []
        target_keywords = keywords or ["coming soon", "launching soon", "new website launch", "software development"]
        target_locations = locations or ["Australia", "India"]

        self.logger.info("Executing Google Custom Search & multi-engine dork queries...")

        for loc in target_locations:
            for kw in target_keywords:
                if len(leads) >= max_results:
                    break

                query = f'"{kw}" "{loc}" email OR contact'
                try:
                    search_results = GoogleSearchClient.search(query, num_results=10, target_country=loc)
                    for res in search_results:
                        if len(leads) >= max_results:
                            break
                        title = res.get("title", "")
                        link = res.get("link", "")
                        snippet = res.get("snippet", "")

                        # Extract clean company name
                        company = title.split("-")[0].split("|")[0].strip()

                        # Extract potential email from snippet
                        found_emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', snippet)
                        email = found_emails[0] if found_emails else ""

                        leads.append(create_standard_lead(
                            company_name=company,
                            lead_source=self.lead_source,
                            source_url=link,
                            website_url=link if "http" in link else "",
                            email=email,
                            city=loc,
                            country=loc,
                            industry="Emerging Tech / Startup",
                            description=snippet
                        ))
                except Exception as e:
                    self.logger.warning(f"Search failed for '{query}': {e}")

        return leads

