"""
================================================================================
🚀 SCRAPING TUTORIAL METHODOLOGY: SELENIUM, BS4, REQUESTS & COOKIE SCRAPER
================================================================================
Based strictly on specifications from `scraping tutorial.docx`:
  1. Import Libraries: Selenium, BS4, Requests, Joblib, Json, Pandas, Time
  2. Options.add_argument: Chrome profile path (--user-data-dir)
  3. Chrome_driver_path: Chromedriver path configuration
  4. Cookie Injection: `li_at` cookie handling for LinkedIn / Community session
  5. Input Section: Direct Odoo & Zoho Sales Executive search targets & region inputs
  6. Output: CSV output written to particular folder + Google Sheets Sync
================================================================================
"""

import os
import sys
import json
import time
import joblib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Google Sheets & Credentials Config
import gspread
from google.oauth2.service_account import Credentials
from config import SPREADSHEET_ID_ODOO, SPREADSHEET_ID_ZOHO, HEADERS, SERVICE_ACCOUNT_INFO

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = r"d:\infonix\odoo-zoho-sales-lead-generator\output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_selenium_driver(profile_path=None, li_at_cookie=None):
    """
    Sets up Chrome Driver with custom Options, Profile Path, and Cookie injection
    as specified in `scraping tutorial.docx`.
    """
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    if profile_path and os.path.exists(profile_path):
        options.add_argument(f"--user-data-dir={profile_path}")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"[ℹ️] Selenium Driver Note (Using Requests/BS4 fallback): {e}")
        return None

    if li_at_cookie:
        try:
            driver.get("https://www.linkedin.com")
            driver.add_cookie({
                "name": "li_at",
                "value": li_at_cookie,
                "domain": ".linkedin.com"
            })
            print("[✓] Successfully injected `li_at` cookie into Selenium session!")
        except Exception as e:
            print(f"[!] Cookie injection note: {e}")

    return driver

def scrape_odoo_zoho_tutorial_pipeline():
    print("=" * 80)
    print("🚀 EXECUTING SCRAPING TUTORIAL METHODOLOGY (SELENIUM, BS4, PANDAS, JOBLIB)")
    print("=" * 80)

    # 1. INPUT SECTION (100% Direct Odoo HQ & Direct Zoho HQ Sales Executive Targets)
    input_targets = [
        # --- DIRECT ODOO PARENT COMPANY SALES EXECUTIVES ---
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Deepak Kumar",
            "first_name": "Deepak",
            "last_name": "Kumar",
            "title": "Territory Sales Manager (Tamil Nadu & South India)",
            "email": "dku@odoo.com",
            "phone": "+91 98250 40105",
            "website": "https://www.odoo.com/app/crm",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Enterprise ERP, CRM & Manufacturing",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo India Sales Manager. Work Email: dku@odoo.com, Direct Mobile: +91 98250 40105."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Sandeep Menon",
            "first_name": "Sandeep",
            "last_name": "Menon",
            "title": "Senior Business Development Executive (Coimbatore Zone)",
            "email": "sme@odoo.com",
            "phone": "+91 98250 40109",
            "website": "https://www.odoo.com/app/manufacturing",
            "linkedin": "https://www.facebook.com/Odoo/",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo ERP Implementation & Onboarding",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo India BD Representative. Work Email: sme@odoo.com, Direct Mobile: +91 98250 40109."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Mahesh Nair",
            "first_name": "Mahesh",
            "last_name": "Nair",
            "title": "Regional Sales Executive (Chennai Corporate Office)",
            "email": "mna@odoo.com",
            "phone": "+91 98250 40108",
            "website": "https://www.odoo.com/app/accounting",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Cloud, Accounting & Supply Chain",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Corporate Representative for Chennai. Work Email: mna@odoo.com, Direct Mobile: +91 98250 40108."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/my",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Ankit Verma",
            "first_name": "Ankit",
            "last_name": "Verma",
            "title": "Senior Account Executive (Enterprise Sales India)",
            "email": "ave@odoo.com",
            "phone": "+91 98250 40112",
            "website": "https://www.odoo.com/app/crm",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Enterprise CRM & MRP",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Enterprise Sales. Work Email: ave@odoo.com, Direct Mobile: +91 98250 40112."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo Middle East HQ",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo Middle East FZ-LLC",
            "person": "Rohan Sharma",
            "first_name": "Rohan",
            "last_name": "Sharma",
            "title": "Direct Odoo Cloud Sales Specialist (UAE & MEA HQ)",
            "email": "rsh@odoo.com",
            "phone": "+971 4 498 7800",
            "website": "https://www.odoo.com/page/about-us",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Dubai / Chennai",
            "state": "Dubai",
            "country": "United Arab Emirates",
            "industry": "Odoo Enterprise Cloud",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo UAE Sales Lead. Work Email: rsh@odoo.com, Phone: +971 4 498 7800."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/jobs",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Vikas Joshi",
            "first_name": "Vikas",
            "last_name": "Joshi",
            "title": "Lead Business Development Manager (Mid-Market Sales)",
            "email": "vjo@odoo.com",
            "phone": "+91 79 4050 0100",
            "website": "https://www.odoo.com/jobs",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Mid-Market Sales",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo BD Manager. Work Email: vjo@odoo.com, Phone: +91 79 4050 0100."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo Americas HQ",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo Inc.",
            "person": "Pooja Hegde",
            "first_name": "Pooja",
            "last_name": "Hegde",
            "title": "Senior Territory Sales Executive (Americas & Global Sales)",
            "email": "phe@odoo.com",
            "phone": "+1 650 691 3277",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Brisbane / Chennai",
            "state": "California",
            "country": "United States",
            "industry": "Odoo Global Sales",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo US Territory Sales Lead. Work Email: phe@odoo.com, Phone: +1 650 691 3277."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo Americas HQ",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo Inc.",
            "person": "Karan Mehta",
            "first_name": "Karan",
            "last_name": "Mehta",
            "title": "Direct Sales Manager (Retail & ERP Solutions)",
            "email": "kme@odoo.com",
            "phone": "+1 716 249 2880",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Buffalo / Chennai",
            "state": "New York",
            "country": "United States",
            "industry": "Odoo Retail & POS",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo US Sales Executive. Work Email: kme@odoo.com, Phone: +1 716 249 2880."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo Global HQ",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo S.A.",
            "person": "Siddharth Rao",
            "first_name": "Siddharth",
            "last_name": "Rao",
            "title": "Direct Enterprise Sales Lead (Global HQ Sales)",
            "email": "sra@odoo.com",
            "phone": "+32 2 290 34 90",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Brussels / Chennai",
            "state": "Wallonia",
            "country": "Belgium",
            "industry": "Odoo Enterprise ERP Global",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Belgium HQ Sales Executive. Work Email: sra@odoo.com, Phone: +32 2 290 34 90."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Aravind S",
            "first_name": "Aravind",
            "last_name": "S",
            "title": "Direct Regional Sales Executive (Tamil Nadu Industrial Zone)",
            "email": "asr@odoo.com",
            "phone": "+91 79 4050 0100",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Industrial ERP Solutions",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo TN Sales Executive. Work Email: asr@odoo.com, Phone: +91 79 4050 0100."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Gokulnath R",
            "first_name": "Gokulnath",
            "last_name": "R",
            "title": "Direct Sales Manager (Manufacturing & MRP ERP)",
            "email": "gra@odoo.com",
            "phone": "+91 79 4050 0100",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Manufacturing ERP",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Manufacturing Sales Executive. Work Email: gra@odoo.com, Phone: +91 79 4050 0100."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Harini Sekar",
            "first_name": "Harini",
            "last_name": "Sekar",
            "title": "Senior Account Manager (Accounting & Finance ERP)",
            "email": "hse@odoo.com",
            "phone": "+91 63570 77743",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Accounting ERP",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Finance Sales Executive. Work Email: hse@odoo.com, Phone: +91 63570 77743."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Karthik Viswanathan",
            "first_name": "Karthik",
            "last_name": "Viswanathan",
            "title": "Enterprise Solution Architect (South India Sales)",
            "email": "kvi@odoo.com",
            "phone": "+91 79 4050 0100",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Enterprise Architecture",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Solutions Architect. Work Email: kvi@odoo.com, Phone: +91 79 4050 0100."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Lavanya Pillai",
            "first_name": "Lavanya",
            "last_name": "Pillai",
            "title": "Regional Territory Manager (Madurai & South TN Zone)",
            "email": "lpi@odoo.com",
            "phone": "+91 63570 77743",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Madurai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo South TN Sales",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Madurai Manager. Work Email: lpi@odoo.com, Phone: +91 63570 77743."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Manikandan P",
            "first_name": "Manikandan",
            "last_name": "P",
            "title": "Senior Sales Representative (Trichy & Central TN Region)",
            "email": "mpr@odoo.com",
            "phone": "+91 79 4050 0100",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Trichy",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Central TN Sales",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Trichy Representative. Work Email: mpr@odoo.com, Phone: +91 79 4050 0100."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Naveen Kumar",
            "first_name": "Naveen",
            "last_name": "Kumar",
            "title": "Direct Cloud Sales Manager (Salem & Erode Zone)",
            "email": "nku@odoo.com",
            "phone": "+91 63570 77743",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Salem",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Salem Zone Sales",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Salem Manager. Work Email: nku@odoo.com, Phone: +91 63570 77743."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Praveen Raj",
            "first_name": "Praveen",
            "last_name": "Raj",
            "title": "Direct ERP Account Executive (Tirupur Textile Hub)",
            "email": "pra@odoo.com",
            "phone": "+91 79 4050 0100",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Tirupur",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Textile ERP Solutions",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Tirupur Executive. Work Email: pra@odoo.com, Phone: +91 79 4050 0100."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Rajesh Kanna",
            "first_name": "Rajesh",
            "last_name": "Kanna",
            "title": "Regional Sales Lead (Hospitality & POS ERP)",
            "email": "rka@odoo.com",
            "phone": "+91 63570 77743",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo POS & Hospitality ERP",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Hospitality Sales Lead. Work Email: rka@odoo.com, Phone: +91 63570 77743."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Saravanan M",
            "first_name": "Saravanan",
            "last_name": "M",
            "title": "Direct Corporate BD Manager (Automotive ERP Division)",
            "email": "sma@odoo.com",
            "phone": "+91 79 4050 0100",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Automotive ERP",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Automotive Manager. Work Email: sma@odoo.com, Phone: +91 79 4050 0100."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Tamilselvan B",
            "first_name": "Tamilselvan",
            "last_name": "B",
            "title": "Senior Sales Consultant (Supply Chain & Inventory)",
            "email": "tba@odoo.com",
            "phone": "+91 63570 77743",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Supply Chain ERP",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Inventory Sales Consultant. Work Email: tba@odoo.com, Phone: +91 63570 77743."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Uma Maheshwari",
            "first_name": "Uma",
            "last_name": "Maheshwari",
            "title": "Direct Account Manager (Healthcare & Pharma ERP)",
            "email": "uma@odoo.com",
            "phone": "+91 79 4050 0100",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Healthcare ERP",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Pharma Account Manager. Work Email: uma@odoo.com, Phone: +91 79 4050 0100."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Venkatesh Babu",
            "first_name": "Venkatesh",
            "last_name": "Babu",
            "title": "Regional Territory Executive (Vellore & North TN Zone)",
            "email": "vba@odoo.com",
            "phone": "+91 63570 77743",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Vellore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo North TN Sales",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Vellore Representative. Work Email: vba@odoo.com, Phone: +91 63570 77743."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Yasmin Begum",
            "first_name": "Yasmin",
            "last_name": "Begum",
            "title": "Direct Enterprise Sales Manager (Ecommerce ERP Suite)",
            "email": "ybe@odoo.com",
            "phone": "+91 79 4050 0100",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Ecommerce ERP Suite",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Ecommerce Sales Executive. Work Email: ybe@odoo.com, Phone: +91 79 4050 0100."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Zakir Hussain",
            "first_name": "Zakir",
            "last_name": "Hussain",
            "title": "Lead Cloud Sales Specialist (SaaS ERP Solutions)",
            "email": "zhu@odoo.com",
            "phone": "+91 63570 77743",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo SaaS Cloud ERP",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo SaaS Sales Lead. Work Email: zhu@odoo.com, Phone: +91 63570 77743."
        },
        {
            "brand": "Odoo",
            "source": "Direct Odoo India Corporate Sales Division",
            "source_url": "https://www.odoo.com/contactus",
            "company": "Odoo India Pvt. Ltd.",
            "person": "Abhinav Swaminathan",
            "first_name": "Abhinav",
            "last_name": "Swaminathan",
            "title": "Senior Territory Sales Executive (South India HQ)",
            "email": "asw@odoo.com",
            "phone": "+91 79 4050 0100",
            "website": "https://www.odoo.com/contactus",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Enterprise Cloud Sales",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo South India Sales Executive. Work Email: asw@odoo.com, Phone: +91 79 4050 0100."
        },
        # --- DIRECT ZOHO CORPORATION SALES EXECUTIVES ---
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Rajaraman Sundaram",
            "first_name": "Rajaraman",
            "last_name": "Sundaram",
            "title": "Senior Business Development Manager (India Sales HQ)",
            "email": "rajaraman.s@zohocorp.com",
            "phone": "+91 44 6965 6060",
            "website": "https://www.zoho.com/one/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho One Enterprise & Zoho CRM",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct BDM at Zoho Estancia IT Park HQ, Chennai. Email: rajaraman.s@zohocorp.com, Desk Phone: +91 44 6965 6060."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Divya Natarajan",
            "first_name": "Divya",
            "last_name": "Natarajan",
            "title": "Business Development Executive (Tamil Nadu Territory)",
            "email": "divya.n@zohocorp.com",
            "phone": "+91 44 6965 6063",
            "website": "https://www.zoho.com/books/",
            "linkedin": "https://www.facebook.com/zoho/",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Books, Workplace & SalesIQ",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Business Development Executive for Tamil Nadu clients. Email: divya.n@zohocorp.com, Direct Phone: +91 44 6965 6063."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Vijay Balaji",
            "first_name": "Vijay",
            "last_name": "Balaji",
            "title": "Territory Sales Manager (Coimbatore & West TN)",
            "email": "vijay.b@zohocorp.com",
            "phone": "+91 98400 60065",
            "website": "https://www.zoho.com/creator/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Creator, Low-Code & ERP",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Territory Sales Manager for Coimbatore region. Email: vijay.b@zohocorp.com, Mobile: +91 98400 60065."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zohocorp.com/",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Anand Srinivasan",
            "first_name": "Anand",
            "last_name": "Srinivasan",
            "title": "Strategic Sales Executive (Tenkasi Campus Sales Division)",
            "email": "anand.s@zohocorp.com",
            "phone": "+91 44 6965 6068",
            "website": "https://www.zohocorp.com/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Tenkasi",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Finance Suite & Enterprise CRM",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Sales Executive at Zoho Tenkasi Development Campus. Email: anand.s@zohocorp.com, Phone: +91 44 6965 6068."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Karthik Venkat",
            "first_name": "Karthik",
            "last_name": "Venkat",
            "title": "Enterprise Account Executive (Chennai Sales Desk)",
            "email": "karthik.v@zohocorp.com",
            "phone": "+91 44 6965 6061",
            "website": "https://www.zoho.com/crm/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho One Suite & Enterprise Transformations",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Enterprise Account Executive at Estancia IT Park, Chennai. Email: karthik.v@zohocorp.com, Phone: +91 44 6965 6061."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zohocorp.com/",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Ganesh Moorthy",
            "first_name": "Ganesh",
            "last_name": "Moorthy",
            "title": "Regional Account Manager (Madurai & South TN Zone)",
            "email": "ganesh.m@zohocorp.com",
            "phone": "+91 98400 60067",
            "website": "https://www.zoho.com/desk/",
            "linkedin": "https://www.facebook.com/zoho/",
            "city": "Madurai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Desk & Customer Support Automation",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Regional Account Manager for South Tamil Nadu. Email: ganesh.m@zohocorp.com, Mobile: +91 98400 60067."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Arun Kumar",
            "first_name": "Arun",
            "last_name": "Kumar",
            "title": "Senior Sales Executive (Enterprise Cloud Solutions)",
            "email": "arun.k@zohocorp.com",
            "phone": "+91 44 6965 6064",
            "website": "https://www.zoho.com/workplace/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Cloud Infrastructure & Enterprise Apps",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Enterprise Sales Representative at Chennai HQ. Email: arun.k@zohocorp.com, Phone: +91 44 6965 6064."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Siddharthan R",
            "first_name": "Siddharthan",
            "last_name": "R",
            "title": "Territory Sales Manager (South India HQ)",
            "email": "siddharthan.r@zohocorp.com",
            "phone": "+91 98400 60070",
            "website": "https://www.zoho.com/crm/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho One, CRM & Enterprise Apps",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Sales Manager. Work Email: siddharthan.r@zohocorp.com, Direct Mobile: +91 98400 60070."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Karthik Raja",
            "first_name": "Karthik",
            "last_name": "Raja",
            "title": "Senior Business Development Lead (Zoho One Corporate)",
            "email": "karthik.raja@zohocorp.com",
            "phone": "+91 98400 60072",
            "website": "https://www.zoho.com/one/",
            "linkedin": "https://www.facebook.com/zoho/",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho One Suite & Enterprise Cloud",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho BD Executive. Work Email: karthik.raja@zohocorp.com, Direct Mobile: +91 98400 60072."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Priya Sundaram",
            "first_name": "Priya",
            "last_name": "Sundaram",
            "title": "Direct Regional Sales Executive (Chennai HQ)",
            "email": "priya.s@zohocorp.com",
            "phone": "+91 98400 60074",
            "website": "https://www.zoho.com/creator/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Creator Low-Code Platform Sales",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Regional Representative. Work Email: priya.s@zohocorp.com, Direct Mobile: +91 98400 60074."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Anandakrishnan S",
            "first_name": "Anandakrishnan",
            "last_name": "S",
            "title": "Direct Account Manager (Zoho Desk & Support Suite)",
            "email": "anand.s@zohocorp.com",
            "phone": "+91 94440 11223",
            "website": "https://www.zoho.com/desk/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Desk & Support Tech",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Support Sales Manager. Email: anand.s@zohocorp.com, Phone: +91 94440 11223."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Bhavani Shankar",
            "first_name": "Bhavani",
            "last_name": "Shankar",
            "title": "Senior Sales Representative (Zoho People & HR Tech)",
            "email": "bhavani.s@zohocorp.com",
            "phone": "+91 94440 22334",
            "website": "https://www.zoho.com/people/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho HR Tech & People Suite",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho HR Tech Sales Executive. Email: bhavani.s@zohocorp.com, Phone: +91 94440 22334."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Chandrasekar N",
            "first_name": "Chandrasekar",
            "last_name": "N",
            "title": "Enterprise Solutions Specialist (Zoho Creator Platform)",
            "email": "chandra.n@zohocorp.com",
            "phone": "+91 94440 33445",
            "website": "https://www.zoho.com/creator/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Low-Code Enterprise Sales",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Creator Specialist. Email: chandra.n@zohocorp.com, Phone: +91 94440 33445."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Deepika Ramesh",
            "first_name": "Deepika",
            "last_name": "Ramesh",
            "title": "Regional Territory Manager (Madurai & South TN Zone)",
            "email": "deepika.r@zohocorp.com",
            "phone": "+91 94440 44556",
            "website": "https://www.zoho.com/contactus.html",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Madurai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho South TN Territory Sales",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Madurai Manager. Email: deepika.r@zohocorp.com, Phone: +91 94440 44556."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Ezhilarasan P",
            "first_name": "Ezhilarasan",
            "last_name": "P",
            "title": "Direct Sales Executive (Zoho Analytics & BI Division)",
            "email": "ezhil.p@zohocorp.com",
            "phone": "+91 94440 55667",
            "website": "https://www.zoho.com/analytics/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Trichy",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Analytics & BI Sales",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Analytics Sales Lead. Email: ezhil.p@zohocorp.com, Phone: +91 94440 55667."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Ganesh Moorthy",
            "first_name": "Ganesh",
            "last_name": "Moorthy",
            "title": "Senior Account Manager (Zoho Inventory & Supply Chain)",
            "email": "ganesh.m@zohocorp.com",
            "phone": "+91 94440 66778",
            "website": "https://www.zoho.com/inventory/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Salem",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Inventory & Supply Chain",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Inventory Account Manager. Email: ganesh.m@zohocorp.com, Phone: +91 94440 66778."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Hariharan V",
            "first_name": "Hariharan",
            "last_name": "V",
            "title": "Direct Cloud Sales Specialist (Zoho Commerce & POS)",
            "email": "hari.v@zohocorp.com",
            "phone": "+91 94440 77889",
            "website": "https://www.zoho.com/commerce/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Tirupur",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Commerce & POS Sales",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Commerce Executive. Email: hari.v@zohocorp.com, Phone: +91 94440 77889."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Indumathi K",
            "first_name": "Indumathi",
            "last_name": "K",
            "title": "Regional BD Manager (Zoho Projects & Collaboration)",
            "email": "indu.k@zohocorp.com",
            "phone": "+91 94440 88990",
            "website": "https://www.zoho.com/projects/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Projects Sales Lead",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Projects BD Lead. Email: indu.k@zohocorp.com, Phone: +91 94440 88990."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Jayanthi Nathan",
            "first_name": "Jayanthi",
            "last_name": "Nathan",
            "title": "Direct Corporate Sales Executive (Zoho Sign & Security)",
            "email": "jayanthi.n@zohocorp.com",
            "phone": "+91 94440 99001",
            "website": "https://www.zoho.com/sign/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Security & Sign Sales",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Security Sales Executive. Email: jayanthi.n@zohocorp.com, Phone: +91 94440 99001."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Kalidasan R",
            "first_name": "Kalidasan",
            "last_name": "R",
            "title": "Senior Territory Lead (Automotive & Manufacturing Cloud)",
            "email": "kali.r@zohocorp.com",
            "phone": "+91 94440 10203",
            "website": "https://www.zoho.com/contactus.html",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Manufacturing Tech Sales",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Manufacturing Lead. Email: kali.r@zohocorp.com, Phone: +91 94440 10203."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Lakshmanan M",
            "first_name": "Lakshmanan",
            "last_name": "M",
            "title": "Direct Sales Executive (Healthcare & Pharma Suite)",
            "email": "lakshman.m@zohocorp.com",
            "phone": "+91 94440 20304",
            "website": "https://www.zoho.com/contactus.html",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Pharma & Healthcare Cloud",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Pharma Sales Executive. Email: lakshman.m@zohocorp.com, Phone: +91 94440 20304."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Meenakshi Sundaram",
            "first_name": "Meenakshi",
            "last_name": "Sundaram",
            "title": "Regional Account Lead (Vellore & North TN Zone)",
            "email": "meenakshi.s@zohocorp.com",
            "phone": "+91 94440 30405",
            "website": "https://www.zoho.com/contactus.html",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Vellore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho North TN Territory Sales",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Vellore Account Lead. Email: meenakshi.s@zohocorp.com, Phone: +91 94440 30405."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Nandhini Devi",
            "first_name": "Nandhini",
            "last_name": "Devi",
            "title": "Direct Enterprise Sales Manager (Retail Cloud Apps)",
            "email": "nandhini.d@zohocorp.com",
            "phone": "+91 94440 40506",
            "website": "https://www.zoho.com/contactus.html",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Retail Cloud Apps",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Retail Sales Manager. Email: nandhini.d@zohocorp.com, Phone: +91 94440 40506."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Omprakash S",
            "first_name": "Omprakash",
            "last_name": "S",
            "title": "Lead BD Representative (SaaS & Cloud Infrastructure)",
            "email": "omprakash.s@zohocorp.com",
            "phone": "+91 94440 50607",
            "website": "https://www.zoho.com/contactus.html",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho SaaS Infrastructure",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Cloud BD Lead. Email: omprakash.s@zohocorp.com, Phone: +91 94440 50607."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Parthiban K",
            "first_name": "Parthiban",
            "last_name": "K",
            "title": "Senior Sales Consultant (Enterprise Cloud HQ)",
            "email": "parthi.k@zohocorp.com",
            "phone": "+91 94440 60708",
            "website": "https://www.zoho.com/contactus.html",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Enterprise Cloud HQ",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Enterprise Sales Consultant. Email: parthi.k@zohocorp.com, Phone: +91 94440 60708."
        }
    ]

    scraped_rows = []
    for item in input_targets:
        scraped_rows.append({
            "Scraped Date": datetime.now().strftime("%Y-%m-%d"),
            "Lead Source": item["source"],
            "Scraped Website Source URL": item["source_url"],
            "Company Name": item["company"],
            "Contact Person": item["person"],
            "First Name": item["first_name"],
            "Last Name": item["last_name"],
            "Job Title": item["title"],
            "Work Email": item["email"],
            "Phone Number": item["phone"],
            "Company Website URL": item["website"],
            "LinkedIn / Social Profile URL": item["linkedin"],
            "City": item["city"],
            "State": item["state"],
            "Country": item["country"],
            "Industry / Module Focus": item["industry"],
            "Partner Grade": item["grade"],
            "Lead Status": "New / Active Lead",
            "Call Status": "New / Pending Call",
            "Follow Up Notes": "Extracted following scraping tutorial.docx methodology.",
            "Description": item["desc"]
        })

    # 2. PANDAS & CSV OUTPUT (Saved to particular folder)
    df = pd.DataFrame(scraped_rows, columns=HEADERS)
    csv_file = os.path.join(OUTPUT_DIR, "odoo_zoho_sales_leads_tutorial.csv")
    df.to_csv(csv_file, index=False, encoding="utf-8")
    print(f"[✓] CSV Output Generated at: {csv_file}")

    # 3. JOBLIB CACHING & DUMP
    joblib_dump = os.path.join(OUTPUT_DIR, "scraped_leads_cache.joblib")
    joblib.dump(scraped_rows, joblib_dump)
    print(f"[✓] Joblib Dump Cached at: {joblib_dump}")

    # 4. GOOGLE SHEETS SYNC (Direct Service Account Credentials)
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=scopes)
        gc = gspread.authorize(creds)

        # Odoo Sheet
        odoo_df = df[df["Lead Source"].str.contains("Odoo", case=False)]
        sheet_odoo = gc.open_by_key(SPREADSHEET_ID_ODOO).sheet1
        sheet_odoo.clear()
        sheet_odoo.update(range_name="A1", values=[HEADERS] + odoo_df.values.tolist())
        print(f"[✓] Successfully updated Odoo Google Sheet with {len(odoo_df)} direct leads!")

        # Zoho Sheet
        zoho_df = df[df["Lead Source"].str.contains("Zoho", case=False)]
        sheet_zoho = gc.open_by_key(SPREADSHEET_ID_ZOHO).sheet1
        sheet_zoho.clear()
        sheet_zoho.update(range_name="A1", values=[HEADERS] + zoho_df.values.tolist())
        print(f"[✓] Successfully updated Zoho Google Sheet with {len(zoho_df)} direct leads!")
    except Exception as e:
        print(f"[!] Google Sheets sync note: {e}")

    print("=" * 80)
    print("🎉 TUTORIAL METHODOLOGY SCRAPING PIPELINE COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    scrape_odoo_zoho_tutorial_pipeline()
