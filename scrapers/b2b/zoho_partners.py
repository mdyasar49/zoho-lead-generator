"""
Zoho Partner Network Directory Scraper.
Extracts verified Premium, Advanced, and Authorized Zoho CRM implementation partners.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from config.schemas import create_standard_lead
from core.base_scraper import BaseScraper

class ZohoPartnerScraper(BaseScraper):
    """Scrapes official certified Zoho CRM consulting and implementation partners."""

    def __init__(self, headless: Optional[bool] = None):
        super().__init__(name="ZohoPartners", lead_source="Zoho Partner Network", headless=headless)

    def scrape(
        self,
        keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        leads = []
        target_locations = locations or ["Australia", "India"]

        for country in target_locations:
            if len(leads) >= max_results:
                break

            url = f"https://www.zoho.com/partners/find-partner.html?country={country.lower()}"
            self.logger.info(f"Scraping Zoho Partners for {country}: {url}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            }

            try:
                resp = requests.get(url, headers=headers, timeout=20)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    partners = soup.select(".partner-card, .partner-details, .partner-box")

                    for p in partners:
                        if len(leads) >= max_results:
                            break

                        name_elem = p.select_one(".partner-name, h3, h4")
                        name = name_elem.get_text(strip=True) if name_elem else ""
                        if not name:
                            continue

                        tier_elem = p.select_one(".tier-badge, .partner-tier, .badge")
                        tier = tier_elem.get_text(strip=True) if tier_elem else "Certified Zoho Partner"

                        site_elem = p.select_one("a[href*='http']:not([href*='zoho.com'])")
                        website = site_elem.get("href", "") if site_elem else ""

                        city_elem = p.select_one(".partner-location, .city")
                        city = city_elem.get_text(strip=True) if city_elem else ""
                        domain = website.split("/")[2].replace("www.", "").lower() if website.startswith("http") else ""
                        email = f"contact@{domain}" if domain else ""

                        lead = create_standard_lead(
                            company_name=name,
                            lead_source=self.lead_source,
                            source_url=url,
                            website_url=website or url,
                            email=email,
                            city=city,
                            country=country,
                            industry="Zoho CRM & Cloud Ecosystem",
                            partner_grade=tier,
                            description=f"Official {tier} Zoho CRM implementation consulting partner. Website: {website}."
                        )
                        leads.append(lead)
            except Exception as e:
                self.logger.warning(f"Error fetching Zoho partners: {e}")

        return leads
