"""
Freelancer.com Project & B2B Lead Scraper.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from config.schemas import create_standard_lead
from core.base_scraper import BaseScraper

class FreelancerScraper(BaseScraper):
    """Scrapes active projects and employer briefs from Freelancer.com."""

    def __init__(self, headless: Optional[bool] = None):
        super().__init__(name="Freelancer", lead_source="Freelancer.com", headless=headless)

    def scrape(
        self,
        keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        max_results: int = 30
    ) -> List[Dict[str, Any]]:
        leads = []
        url = "https://www.freelancer.com/jobs"
        self.logger.info(f"Scraping Freelancer projects from {url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                project_cards = soup.select(".JobSearchCard-item, .Project-card, .search-result-item")

                for card in project_cards:
                    if len(leads) >= max_results:
                        break

                    title_elem = card.select_one(".JobSearchCard-primary-heading-link, h2 a, .project-title")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    if not title:
                        continue

                    link = "https://www.freelancer.com" + title_elem.get("href", "") if title_elem else url
                    desc_elem = card.select_one(".JobSearchCard-primary-description, p.desc")
                    desc = desc_elem.get_text(strip=True) if desc_elem else "Project brief"

                    leads.append(create_standard_lead(
                        company_name=f"Freelancer Client ({title[:25]}...)",
                        lead_source=self.lead_source,
                        source_url=link,
                        job_title=title,
                        country="Australia",
                        industry="Custom Software Development",
                        description=desc
                    ))
        except Exception as e:
            self.logger.warning(f"Error scraping Freelancer.com: {e}")

        return leads
