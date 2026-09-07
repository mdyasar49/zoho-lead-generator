"""
Scheduled Automation Cron Entrypoint for Data Scraping Suite.
Ideal for GitHub Actions or Windows Task Scheduler.
"""

import time
import sys
from datetime import datetime
from config.settings import settings
from core.logger import setup_logger
from scrapers import SCRAPERS_REGISTRY

logger = setup_logger("CronPipeline")

def execute_hourly_cron():
    start_time = datetime.now()
    logger.info(f"========== [CRON START] Triggered at {start_time.strftime('%Y-%m-%d %H:%M:%S')} ==========")

    total_leads = 0
    successful_scrapers = 0
    failed_scrapers = 0

    # Key high-yield scrapers for routine automated batch
    priority_scrapers = [
        "odoo_partners",
        "zoho_partners",
        "upwork",
        "linkedin",
        "clutch",
        "serper_social"
    ]

    for name in priority_scrapers:
        scraper_cls = SCRAPERS_REGISTRY.get(name)
        if not scraper_cls:
            continue

        try:
            scraper = scraper_cls(headless=True)
            result = scraper.run(max_results=25)
            if result.get("status") == "Success":
                successful_scrapers += 1
                total_leads += result.get("leads_count", 0)
            else:
                failed_scrapers += 1
        except Exception as e:
            logger.error(f"Cron execution error on {name}: {e}")
            failed_scrapers += 1

    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    logger.info(
        f"========== [CRON FINISHED] Total Leads: {total_leads} | Successful: {successful_scrapers} | Failed: {failed_scrapers} | Duration: {round(elapsed, 2)}s =========="
    )

if __name__ == "__main__":
    execute_hourly_cron()
