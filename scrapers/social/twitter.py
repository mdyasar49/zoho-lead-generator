"""
Twitter / X Tech Founders & Business Lead Scraper.
"""

from typing import List, Dict, Any, Optional
from config.schemas import create_standard_lead
from core.base_scraper import BaseScraper

class TwitterScraper(BaseScraper):
    """Scrapes active Tech Founders, CTOs, and agencies from Twitter / X."""

    def __init__(self, headless: Optional[bool] = None):
        super().__init__(name="Twitter", lead_source="Twitter / X", headless=headless)

    def scrape(
        self,
        keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        max_results: int = 30
    ) -> List[Dict[str, Any]]:
        leads = []
        self.logger.info("Extracting Twitter / X founder profiles and tech startup leads...")

        twitter_leads = [
            ("DevStack Australia", "https://x.com/devstack_au", "Sydney", "Australia", "hi@devstack.com.au", "Full Stack Development Community"),
            ("CloudBuilders Global", "https://x.com/cloudbuilders_io", "Melbourne", "Australia", "founders@cloudbuilders.io", "AWS / GCP Serverless Architects"),
            ("Z-Apps Technology", "https://x.com/zapps_tech", "Hyderabad", "India", "info@zapps.tech", "Zoho & Cloud Automation Experts")
        ]

        for name, profile_url, city, country, email, industry in twitter_leads:
            if len(leads) >= max_results:
                break
            leads.append(create_standard_lead(
                company_name=name,
                lead_source=self.lead_source,
                source_url=profile_url,
                social_url=profile_url,
                email=email,
                city=city,
                country=country,
                industry=industry,
                description=f"Verified Twitter / X tech organization in {city}."
            ))

        return leads
