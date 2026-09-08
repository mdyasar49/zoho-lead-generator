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

        COUNTRY_SLUGS = {
            "australia": "australia-11",
            "india": "india-101",
            "united states": "united-states-225",
            "united kingdom": "united-kingdom-224"
        }

        for country in target_locations:
            if len(leads) >= max_results:
                break

            country_slug = COUNTRY_SLUGS.get(country.lower(), country.lower().replace(" ", "-"))
            url = f"https://www.odoo.com/partners/country/{country_slug}"
            self.logger.info(f"Scraping Odoo Partners for {country}: {url}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            }

            try:
                resp = requests.get(url, headers=headers, timeout=20)
                if resp.status_code != 200:
                    url = f"https://www.odoo.com/partners"
                    resp = requests.get(url, headers=headers, timeout=20)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    partner_links = [
                        a.get("href") for a in soup.find_all("a")
                        if a.get("href", "").startswith("/partners/") and not any(p in a.get("href", "") for p in ["/country/", "?industry=", "?grade="])
                    ]
                    
                    seen_urls = set()
                    for rel_url in partner_links:
                        if len(leads) >= max_results:
                            break
                        if rel_url in seen_urls:
                            continue
                        seen_urls.add(rel_url)
                        
                        full_partner_url = f"https://www.odoo.com{rel_url}" if rel_url.startswith("/") else rel_url
                        try:
                            p_resp = requests.get(full_partner_url, headers=headers, timeout=10)
                            if p_resp.status_code == 200:
                                p_soup = BeautifulSoup(p_resp.text, "html.parser")
                                raw_title = p_soup.title.get_text(strip=True) if p_soup.title else ""
                                comp_name = raw_title.split("|")[0].split("-")[0].strip() or "Odoo Partner"
                                
                                website = ""
                                phone = ""
                                email = ""
                                
                                for a in p_soup.find_all("a"):
                                    href = a.get("href", "")
                                    if href.startswith("tel:"):
                                        phone = href.replace("tel:", "").strip()
                                    elif "mailto:" in href:
                                        email = href.replace("mailto:", "").split("?")[0].strip()
                                    elif href.startswith("http") and not any(ign in href for ign in ["odoo.com", "odoo.sh", "github.com", "youtube.com", "twitter.com", "linkedin.com", "instagram.com", "facebook.com", "tiktok.com", "wa.me"]):
                                        if not website:
                                            website = href
                                
                                # Extract domain email fallback if email is not explicit
                                if not email and website:
                                    domain = website.split("/")[2].replace("www.", "").lower()
                                    email = f"contact@{domain}"
                                
                                grade = "Gold Partner" if "Gold" in p_soup.get_text() else ("Silver Partner" if "Silver" in p_soup.get_text() else "Certified Partner")
                                
                                lead = create_standard_lead(
                                    company_name=comp_name,
                                    lead_source=self.lead_source,
                                    source_url=full_partner_url,
                                    website_url=website or full_partner_url,
                                    email=email,
                                    phone=phone,
                                    city=country,
                                    country=country,
                                    industry="ERP & Odoo Solutions",
                                    partner_grade=grade,
                                    description=f"Official {grade} Odoo ERP implementation partner in {country}. Website: {website}, Phone: {phone}."
                                )
                                leads.append(lead)
                        except Exception as pe:
                            self.logger.warning(f"Error fetching partner detail {full_partner_url}: {pe}")

            except Exception as e:
                self.logger.warning(f"Error fetching Odoo partners for {country}: {e}")

        return leads
