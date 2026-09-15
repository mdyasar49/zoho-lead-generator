"""
Upwork Job Postings & Client Lead Scraper.
"""

import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from config.schemas import create_standard_lead
from core.base_scraper import BaseScraper

class UpworkScraper(BaseScraper):
    """Scrapes active job openings, client briefs, and direct hiring leads from Upwork."""

    def __init__(self, headless: Optional[bool] = None):
        super().__init__(name="Upwork", lead_source="Upwork Job Leads", headless=headless)

    def scrape(
        self,
        keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        leads = []
        target_keywords = keywords or ["python", "react", "erp", "odoo", "zoho"]

        for kw in target_keywords:
            if len(leads) >= max_results:
                break

            query = kw.replace(" ", "+")
            url = f"https://www.upwork.com/nx/search/jobs/?q={query}&sort=recency"
            self.logger.info(f"Scraping Upwork jobs for '{kw}': {url}")

            # Try browser automation first if available
            try:
                driver = self.start_browser()
                driver.get(url)
                time.sleep(3)

                job_elements = driver.find_elements("css selector", "article.job-tile, section.air3-card-section")
                for job in job_elements:
                    if len(leads) >= max_results:
                        break

                    try:
                        title_elem = job.find_element("css selector", "h2.job-tile-title a, a.up-n-link")
                        title = title_elem.text.strip()
                        job_link = title_elem.get_attribute("href")
                        
                        desc_elem = job.find_element("css selector", ".job-description, .air3-line-clamp")
                        desc = desc_elem.text.strip() if desc_elem else ""

                        leads.append(create_standard_lead(
                            company_name=f"Upwork Client ({title[:30]}...)",
                            lead_source=self.lead_source,
                            source_url=job_link or url,
                            job_title=title,
                            country="Australia",
                            industry="Freelance / Contract IT",
                            description=desc or f"Upwork active project looking for {kw} expertise."
                        ))
                    except Exception:
                        continue

            except Exception as e:
                self.logger.warning(f"Browser scrape encountered challenge: {e}")

        return leads
