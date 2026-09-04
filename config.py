"""
================================================================================
🚀 CENTRALIZED ENTERPRISE CONFIGURATION MANAGER
================================================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from workspace root or project dir
env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    env_path = Path(r"d:\infonix\.env")

load_dotenv(dotenv_path=env_path)

# Google Sheets Configuration
SPREADSHEET_ID_ODOO = os.getenv("SPREADSHEET_ID_ODOO", "1X_8LbsHisyvoCfjSuTX5yRVsRgXPDEmu3W5RWXuAC1o")
SPREADSHEET_ID_ZOHO = os.getenv("SPREADSHEET_ID_ZOHO", "18oHqPuo6BhAgI5e_GLSSps5fSc_DpzYEYofgPKxBv9o")
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE", r"d:\infonix\sheet-sync-504707-85df40232946.json")

# Odoo Community Login Credentials
ODOO_COMMUNITY_USERNAME = os.getenv("ODOO_COMMUNITY_USERNAME", "")
ODOO_COMMUNITY_PASSWORD = os.getenv("ODOO_COMMUNITY_PASSWORD", "")
ODOO_LOGIN_URL = "https://www.odoo.com/web/login"
ODOO_COMMUNITY_URL = "https://www.odoo.com/forum"

# Zoho Community Login Credentials
ZOHO_COMMUNITY_USERNAME = os.getenv("ZOHO_COMMUNITY_USERNAME", "")
ZOHO_COMMUNITY_PASSWORD = os.getenv("ZOHO_COMMUNITY_PASSWORD", "")
ZOHO_LOGIN_URL = "https://accounts.zoho.com/signin"
ZOHO_COMMUNITY_URL = "https://help.zoho.com/portal/en/community"

# CRM Standard Schema Columns (21 Columns)
HEADERS = [
    "Scraped Date",
    "Lead Source",
    "Scraped Website Source URL",
    "Company Name",
    "Contact Person",
    "First Name",
    "Last Name",
    "Job Title",
    "Work Email",
    "Phone Number",
    "Company Website URL",
    "LinkedIn / Social Profile URL",
    "City",
    "State",
    "Country",
    "Industry / Module Focus",
    "Partner Grade",
    "Lead Status",
    "Call Status",
    "Follow Up Notes",
    "Description"
]
