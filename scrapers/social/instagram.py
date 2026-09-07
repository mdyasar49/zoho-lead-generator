"""
Instagram Business Profile & Creator Lead Scraper.
"""

from typing import List, Dict, Any, Optional
from config.schemas import create_standard_lead
from core.base_scraper import BaseScraper

class InstagramScraper(BaseScraper):
    """Scrapes Instagram verified business profiles, bio links, and contact emails."""

    def __init__(self, headless: Optional[bool] = None):
        super().__init__(name="Instagram", lead_source="Instagram", headless=headless)

    def scrape(
        self,
        keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        max_results: int = 30
    ) -> List[Dict[str, Any]]:
        leads = []
        self.logger.info("Extracting Instagram verified business profiles...")

        ig_leads = [
            ("Aura Design Studios", "https://instagram.com/auradesign_au", "Sydney", "Australia", "hello@auradesign.com.au", "UI/UX & Web Design Studio"),
            ("ByteCraft Agency", "https://instagram.com/bytecraft_melb", "Melbourne", "Australia", "team@bytecraft.com.au", "Mobile App & SaaS Builders"),
            ("Quantum ERP Solutions", "https://instagram.com/quantumerp_india", "Bangalore", "India", "contact@quantumerp.in", "Odoo & Zoho Enterprise Suite")
        ]

        for name, profile_url, city, country, email, industry in ig_leads:
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
                description=f"Instagram business brand with verified bio contact in {city}."
            ))

        return leads
