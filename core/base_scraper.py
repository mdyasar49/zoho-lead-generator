"""
================================================================================
🚀 CENTRALIZED BASE SCRAPER FRAMEWORK
================================================================================
All platform scrapers inherit from BaseScraper.
Provides lifecycle orchestration, automated error handling, validation, and export!
"""

import time
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from selenium import webdriver

from config.settings import settings
from config.schemas import create_standard_lead
from core.browser import BrowserManager
from core.verifier import LeadVerifier
from core.exporter import DataExporter
from core.logger import setup_logger

class BaseScraper(ABC):
    """Abstract Base Class for all platform scrapers."""

    def __init__(self, name: str, lead_source: str, headless: Optional[bool] = None):
        self.name = name
        self.lead_source = lead_source
        self.headless = settings.HEADLESS if headless is None else headless
        self.logger = setup_logger(self.name)
        self.driver: Optional[webdriver.Chrome] = None
        self.scraped_leads: List[Dict[str, Any]] = []

    def start_browser(self, custom_user_agent: Optional[str] = None) -> webdriver.Chrome:
        """Initializes the browser session if not already open."""
        if not self.driver:
            self.logger.info(f"Launching browser for {self.name}...")
            self.driver = BrowserManager.create_driver(
                headless=self.headless,
                custom_user_agent=custom_user_agent
            )
        return self.driver

    def close_browser(self):
        """Safely terminates the browser."""
        if self.driver:
            BrowserManager.safe_quit(self.driver)
            self.driver = None

    @abstractmethod
    def scrape(
        self,
        keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Abstract method to be implemented by each platform scraper.
        Should return a list of raw or structured lead dictionaries.
        """
        pass

    def validate_and_enrich(self, leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Passes all leads through the central LeadVerifier and strictly drops
        any lead that does not have a 100% verified, deliverable email.
        Zero tolerance for bouncing or invalid email addresses.
        """
        self.logger.info(f"Validating and filtering {len(leads)} leads for zero-bounce deliverability...")
        valid_leads = []
        for lead in leads:
            email = (
                lead.get("Work Email") or
                lead.get("Primary Work Email") or
                lead.get("Email") or
                lead.get("email") or
                lead.get("verified_email") or
                ""
            ).strip().lower()

            if not email or "@" not in email:
                self.logger.warning(f"Dropping lead '{lead.get('Company Name') or 'Unknown'}' - No email found.")
                continue

            is_valid, reason = LeadVerifier.verify_email(email)
            if not is_valid:
                self.logger.warning(f"Dropping bouncing/undeliverable lead '{lead.get('Company Name') or 'Unknown'}' (Email: {email}) - Reason: {reason}")
                continue

            validated = LeadVerifier.enrich_and_validate(lead)
            valid_leads.append(validated)

        self.logger.info(f"Retained {len(valid_leads)}/{len(leads)} verified deliverable leads (Purged all undeliverable/bouncing leads).")
        return valid_leads

    def export(self, leads: List[Dict[str, Any]], spreadsheet_id: Optional[str] = None) -> Dict[str, Any]:
        """Exports leads through the central exporter."""
        return DataExporter.export_all(
            leads=leads,
            source_name=self.name,
            spreadsheet_id=spreadsheet_id
        )

    def run(
        self,
        keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        max_results: int = 50,
        spreadsheet_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Standard complete execution lifecycle:
        1. Start Scraper
        2. Scrape Data
        3. Validate & Enrich Leads
        4. Multi-Channel Export
        5. Clean up & Return Metrics
        """
        start_time = time.time()
        self.logger.info(f"========== Starting Scraper: {self.name} ==========")

        try:
            raw_leads = self.scrape(
                keywords=keywords or settings.DEFAULT_KEYWORDS,
                locations=locations or settings.TARGET_REGIONS,
                max_results=max_results
            )

            validated_leads = self.validate_and_enrich(raw_leads)
            self.scraped_leads = validated_leads

            export_metrics = self.export(validated_leads, spreadsheet_id=spreadsheet_id)

            duration = round(time.time() - start_time, 2)
            self.logger.info(
                f"========== Completed {self.name} in {duration}s. Scraped: {len(validated_leads)} leads =========="
            )

            return {
                "scraper": self.name,
                "status": "Success",
                "leads_count": len(validated_leads),
                "duration_seconds": duration,
                "export_metrics": export_metrics,
                "leads": validated_leads
            }

        except Exception as e:
            self.logger.error(f"Scraper execution failed: {e}", exc_info=True)
            return {
                "scraper": self.name,
                "status": "Failed",
                "error": str(e),
                "leads_count": 0,
                "leads": []
            }
        finally:
            self.close_browser()
