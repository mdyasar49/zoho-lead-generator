"""
================================================================================
🚀 CENTRALIZED ENTERPRISE SETTINGS & SINGLE SOURCE OF TRUTH
================================================================================
Changing settings in this file or the `.env` file automatically applies
across every platform scraper and utility in the entire project!
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = PROJECT_ROOT.parent

# Search and load .env from multiple probable locations
env_candidates = [
    PROJECT_ROOT / ".env",
    WORKSPACE_ROOT / ".env",
    PROJECT_ROOT / "config" / ".env"
]

for candidate in env_candidates:
    if candidate.exists():
        load_dotenv(dotenv_path=candidate, override=False)

class Settings:
    """Master centralized configuration registry for all scrapers."""

    # -------------------------------------------------------------
    # 1. Project & Environment Meta
    # -------------------------------------------------------------
    ENV: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    PROJECT_NAME: str = "Enterprise Unified Data Scraping Engine"
    VERSION: str = "2.0.0"

    # -------------------------------------------------------------
    # 2. Browser & Anti-Detection Automation Settings
    # -------------------------------------------------------------
    HEADLESS: bool = os.getenv("HEADLESS", "True").lower() in ("true", "1", "yes")
    BROWSER_TIMEOUT: int = int(os.getenv("BROWSER_TIMEOUT", "30"))
    PAGE_LOAD_DELAY: float = float(os.getenv("PAGE_LOAD_DELAY", "2.5"))
    USER_DATA_DIR: str = os.getenv("USER_DATA_DIR", str(PROJECT_ROOT / ".browser_profile"))
    ENABLE_STEALTH: bool = os.getenv("ENABLE_STEALTH", "True").lower() in ("true", "1", "yes")
    PROXY_URL: str = os.getenv("PROXY_URL", "")  # e.g., http://user:pass@host:port

    # -------------------------------------------------------------
    # 3. Google Sheets Integration Settings
    # -------------------------------------------------------------
    AUTO_SYNC_GOOGLE_SHEETS: bool = os.getenv("AUTO_SYNC_GOOGLE_SHEETS", "True").lower() in ("true", "1", "yes")
    
    # Priority default sheet IDs
    SPREADSHEET_ID_MASTER: str = os.getenv(
        "SPREADSHEET_ID_MASTER",
        os.getenv("SPREADSHEET_ID", "1QY8hbycY-gdOWRch52SKoUS975U-t3EgZ0JrtdhPCoM")
    )
    SPREADSHEET_ID_ODOO: str = os.getenv("SPREADSHEET_ID_ODOO", "1X_8LbsHisyvoCfjSuTX5yRVsRgXPDEmu3W5RWXuAC1o")
    SPREADSHEET_ID_ZOHO: str = os.getenv("SPREADSHEET_ID_ZOHO", "18oHqPuo6BhAgI5e_GLSSps5fSc_DpzYEYofgPKxBv9o")
    SPREADSHEET_ID_SOCIAL: str = os.getenv("SPREADSHEET_ID_SOCIAL", "10n8gWkv7Q2vYpW3U_vI5-4f4l_1Q2vYpW3U_vI5-4f")

    CREDENTIALS_FILE: str = os.getenv(
        "CREDENTIALS_FILE",
        str(WORKSPACE_ROOT / "sheet-sync-504707-85df40232946.json")
    )

    # -------------------------------------------------------------
    # 4. Zoho CRM Direct API Integration
    # -------------------------------------------------------------
    AUTO_SYNC_ZOHO_CRM: bool = os.getenv("AUTO_SYNC_ZOHO_CRM", "False").lower() in ("true", "1", "yes")
    ZOHO_CLIENT_ID: str = os.getenv("ZOHO_CLIENT_ID", "")
    ZOHO_CLIENT_SECRET: str = os.getenv("ZOHO_CLIENT_SECRET", "")
    ZOHO_REFRESH_TOKEN: str = os.getenv("ZOHO_REFRESH_TOKEN", "")
    ZOHO_ORG_ID: str = os.getenv("ZOHO_ORG_ID", "")
    ZOHO_API_DOMAIN: str = os.getenv("ZOHO_API_DOMAIN", "https://www.zohoapis.com")

    # -------------------------------------------------------------
    # 5. Odoo CRM / Portal Integration
    # -------------------------------------------------------------
    ODOO_URL: str = os.getenv("ODOO_URL", "https://app.canadiancrystalline.info")
    ODOO_DB: str = os.getenv("ODOO_DB", "app365")
    ODOO_USERNAME: str = os.getenv("ODOO_USERNAME", "admin")
    ODOO_PASSWORD: str = os.getenv("ODOO_PASSWORD", "admin")

    # -------------------------------------------------------------
    # 6. External APIs (Serper & Gemini AI)
    # -------------------------------------------------------------
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # -------------------------------------------------------------
    # 7. Default Scraping Search Parameters
    # -------------------------------------------------------------
    TARGET_REGIONS: List[str] = [
        "Australia",
        "India",
        "United States",
        "United Kingdom"
    ]

    TARGET_CITIES: List[str] = [
        "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide",
        "Bangalore", "Chennai", "Mumbai", "Hyderabad", "Delhi NCR"
    ]

    DEFAULT_KEYWORDS: List[str] = [
        "Software Development",
        "Web Development",
        "ERP Implementation",
        "Odoo Partner",
        "Zoho CRM Consultant",
        "coming soon",
        "launching soon",
        "new launch"
    ]

    # -------------------------------------------------------------
    # 8. Local Export Settings
    # -------------------------------------------------------------
    OUTPUT_DIR: Path = PROJECT_ROOT / "output"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"

    def __init__(self):
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    def get_service_account_info(self) -> Dict[str, Any]:
        """Loads Service Account credentials safely from file or fallback."""
        if os.path.exists(self.CREDENTIALS_FILE):
            try:
                with open(self.CREDENTIALS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Check project root fallback credentials.json
        fallback_file = PROJECT_ROOT / "credentials.json"
        if fallback_file.exists():
            try:
                with open(fallback_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        # Fallback dictionary
        return {
            "type": "service_account",
            "project_id": "sheet-sync-504707",
            "private_key_id": "85df40232946fa2bc19eacb228794511c7736d64",
            "client_email": "sheet-sync@sheet-sync-504707.iam.gserviceaccount.com",
            "client_id": "108318505235340636027",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sheet-sync%40sheet-sync-504707.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }

# Global singleton settings object
settings = Settings()
