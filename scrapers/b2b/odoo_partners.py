"""
Odoo Official Partners Directory Scraper.
Extracts verified Gold, Silver, and Ready Odoo ERP implementation partners.
"""

import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from config.schemas import create_standard_lead
from core.base_scraper import BaseScraper

class OdooPartnerScraper(BaseScraper):
    """Scrapes official certified Odoo ERP implementation partners globally."""

    def __init__(self, headless: Optional[bool] = None):
        super().__init__(name="OdooPartners", lead_source="Odoo Partner Directory", headless=headless)

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

            country_slug = country.lower().replace(" ", "-")
            url = f"https://www.odoo.com/partners/country/{country_slug}"
            self.logger.info(f"Scraping Odoo Partners for {country}: {url}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            }

            try:
                resp = requests.get(url, headers=headers, timeout=20)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    partner_cards = soup.select(".o_partner_card, .o_partner_item, div[itemtype*='Organization']")

                    for card in partner_cards:
                        if len(leads) >= max_results:
                            break

                        name_elem = card.select_one("h3, .o_partner_name, a[itemprop='name']")
                        name = name_elem.get_text(strip=True) if name_elem else ""
                        if not name:
                            continue

                        grade_elem = card.select_one(".badge, .o_partner_grade, .o_partner_tier")
                        grade = grade_elem.get_text(strip=True) if grade_elem else "Certified Partner"

                        site_elem = card.select_one("a[href*='http']:not([href*='odoo.com'])")
                        website = site_elem.get("href", "") if site_elem else ""

                        city_elem = card.select_one(".o_partner_city, span[itemprop='addressLocality']")
                        city = city_elem.get_text(strip=True) if city_elem else ""

                        lead = create_standard_lead(
                            company_name=name,
                            lead_source=self.lead_source,
                            source_url=url,
                            company_website_url=website,
                            city=city,
                            country=country,
                            industry="ERP & Odoo Solutions",
                            partner_grade=grade,
                            description=f"Official {grade} Odoo ERP implementation partner in {country}."
                        )
                        leads.append(lead)

            except Exception as e:
                self.logger.warning(f"Error fetching Odoo partners for {country}: {e}")

        return leads
