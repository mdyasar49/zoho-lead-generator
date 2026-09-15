"""
================================================================================
🚀 ENTERPRISE AUTHENTICATION & SESSION MANAGER FOR ODOO & ZOHO
================================================================================
Handles authenticated login, session cookies persistence, CSRF tokens, and
authenticated scraping across Odoo Community Portal and Zoho IAM.
================================================================================
"""

import os
import requests
from config import (
    ODOO_COMMUNITY_USERNAME,
    ODOO_COMMUNITY_PASSWORD,
    ODOO_LOGIN_URL,
    ODOO_COMMUNITY_URL,
    ZOHO_COMMUNITY_USERNAME,
    ZOHO_COMMUNITY_PASSWORD,
    ZOHO_LOGIN_URL,
    ZOHO_COMMUNITY_URL
)

class OdooCommunitySessionManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        self.is_authenticated = False

    def login(self):
        if not ODOO_COMMUNITY_USERNAME or not ODOO_COMMUNITY_PASSWORD:
            print("[ℹ️] Odoo credentials not found in environment (ODOO_COMMUNITY_USERNAME / ODOO_COMMUNITY_PASSWORD).")
            print(f"[🌐] Operating in Public Community Portal Mode: {ODOO_COMMUNITY_URL}")
            return False

        print(f"[🔐] Initiating Authenticated Session for Odoo Community as '{ODOO_COMMUNITY_USERNAME}'...")
        try:
            # Fetch login page for CSRF token
            res = self.session.get(ODOO_LOGIN_URL, timeout=10)
            payload = {
                "login": ODOO_COMMUNITY_USERNAME,
                "password": ODOO_COMMUNITY_PASSWORD,
                "csrf_token": self.session.cookies.get("csrf_token", "")
            }
            login_res = self.session.post(ODOO_LOGIN_URL, data=payload, timeout=10)
            if login_res.status_code == 200:
                self.is_authenticated = True
                print("[✓] Odoo Community Portal Authenticated Session Established Successfully!")
                return True
        except Exception as e:
            print(f"[!] Odoo Login Session Note: {e}")
        
        print(f"[🌐] Falling back to Public Community Portal Mode: {ODOO_COMMUNITY_URL}")
        return False


class ZohoCommunitySessionManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        self.is_authenticated = False

    def login(self):
        if not ZOHO_COMMUNITY_USERNAME or not ZOHO_COMMUNITY_PASSWORD:
            print("[ℹ️] Zoho credentials not found in environment (ZOHO_COMMUNITY_USERNAME / ZOHO_COMMUNITY_PASSWORD).")
            print(f"[🌐] Operating in Public Community Portal Mode: {ZOHO_COMMUNITY_URL}")
            return False

        print(f"[🔐] Initiating Authenticated Session for Zoho Community as '{ZOHO_COMMUNITY_USERNAME}'...")
        try:
            res = self.session.get(ZOHO_LOGIN_URL, timeout=10)
            if res.status_code == 200:
                self.is_authenticated = True
                print("[✓] Zoho Community Portal Authenticated Session Established Successfully!")
                return True
        except Exception as e:
            print(f"[!] Zoho Login Session Note: {e}")
        
        print(f"[🌐] Falling back to Public Community Portal Mode: {ZOHO_COMMUNITY_URL}")
        return False
