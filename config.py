"""
================================================================================
🚀 CENTRALIZED ENTERPRISE CONFIGURATION MANAGER
================================================================================
"""

import os
import json
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

# Service Account Dictionary Loader (Prefers Direct File, Fallbacks to Direct Dict)
if os.path.exists(CREDENTIALS_FILE):
    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
        SERVICE_ACCOUNT_INFO = json.load(f)
else:
    SERVICE_ACCOUNT_INFO = {
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
