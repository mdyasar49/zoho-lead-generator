"""
PeoplePerHour UK/AU Freelance & Contract Lead Scraper.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from config.schemas import create_standard_lead
from core.base_scraper import BaseScraper

class PeoplePerHourScraper(BaseScraper):
    """Scrapes freelance projects and client opportunities from PeoplePerHour."""

    def __init__(self, headless: Optional[bool] = None):
        super().__init__(name="PeoplePerHour", lead_source="PeoplePerHour", headless=headless)

    def scrape(
        self,
        keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        max_results: int = 30
    ) -> List[Dict[str, Any]]:
        leads = []
        url = "https://www.peopleperhour.com/freelance-jobs"
        self.logger.info(f"Scraping PeoplePerHour from {url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                items = soup.select(".item, .job-item, .project-card")

                for item in items:
                    if len(leads) >= max_results:
                        break

                    title_elem = item.select_one("h6 a, .title a, h2 a")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    if not title:
                        continue

                    link = title_elem.get("href", url)
                    desc_elem = item.select_one(".desc, .snippet, p")
                    desc = desc_elem.get_text(strip=True) if desc_elem else "Project listing"

                    leads.append(create_standard_lead(
                        company_name=f"PPH Buyer ({title[:25]}...)",
                        lead_source=self.lead_source,
                        source_url=link,
                        job_title=title,
                        country="Australia",
                        industry="IT & Web Development",
                        description=desc
                    ))
        except Exception as e:
            self.logger.warning(f"Error scraping PeoplePerHour: {e}")

        return leads
