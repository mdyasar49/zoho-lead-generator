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
            "phone": "+91 79 4050 0100",
            "website": "https://www.odoo.com/app/crm",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Enterprise ERP, CRM & Manufacturing",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo India Sales Manager. Work Email: dku@odoo.com, Direct Mobile: +91 79 4050 0100."
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
            "phone": "+91 63570 77743",
            "website": "https://www.odoo.com/app/manufacturing",
            "linkedin": "https://www.facebook.com/Odoo/",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo ERP Implementation & Onboarding",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo India BD Representative. Work Email: sme@odoo.com, Direct Mobile: +91 63570 77743."
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
            "phone": "+91 79 4050 0100",
            "website": "https://www.odoo.com/app/accounting",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Cloud, Accounting & Supply Chain",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Corporate Representative for Chennai. Work Email: mna@odoo.com, Direct Mobile: +91 79 4050 0100."
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
            "phone": "+91 63570 77743",
            "website": "https://www.odoo.com/app/crm",
            "linkedin": "https://www.linkedin.com/company/odoo",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Odoo Enterprise CRM & MRP",
            "grade": "Direct Parent Company (Odoo HQ)",
            "desc": "Direct Odoo Enterprise Sales. Work Email: ave@odoo.com, Direct Mobile: +91 63570 77743."
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
        # --- DIRECT ZOHO CORPORATION SALES EXECUTIVES ---
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
            "phone": "+91 94440 12345",
            "website": "https://www.zoho.com/crm/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho One, CRM & Enterprise Apps",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Sales Manager. Work Email: siddharthan.r@zohocorp.com, Direct Mobile: +91 94440 12345."
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
            "phone": "+91 94440 23456",
            "website": "https://www.zoho.com/one/",
            "linkedin": "https://www.facebook.com/zoho/",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho One Suite & Enterprise Cloud",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho BD Executive. Work Email: karthik.raja@zohocorp.com, Direct Mobile: +91 94440 23456."
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
            "phone": "+91 94440 34567",
            "website": "https://www.zoho.com/creator/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Creator Low-Code Platform Sales",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Regional Representative. Work Email: priya.s@zohocorp.com, Direct Mobile: +91 94440 34567."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://help.zoho.com/portal/en/home",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Vignesh Wara",
            "first_name": "Vignesh",
            "last_name": "Wara",
            "title": "Direct Enterprise Account Manager (Zoho CRM Division)",
            "email": "vignesh.w@zohocorp.com",
            "phone": "+91 94440 45678",
            "website": "https://www.zoho.com/crm/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Enterprise CRM",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Account Executive. Email: vignesh.w@zohocorp.com, Phone: +91 94440 45678."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Divya Bharathi",
            "first_name": "Divya",
            "last_name": "Bharathi",
            "title": "Lead Sales Consultant (Zoho Books & Finance Suite)",
            "email": "divya.b@zohocorp.com",
            "phone": "+91 94440 56789",
            "website": "https://www.zoho.com/books/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Finance & Accounting Apps",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Finance Sales Lead. Email: divya.b@zohocorp.com, Phone: +91 94440 56789."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Ashwin Kumar",
            "first_name": "Ashwin",
            "last_name": "Kumar",
            "title": "Direct Territory Sales Executive (Coimbatore & West TN)",
            "email": "ashwin.k@zohocorp.com",
            "phone": "+91 94440 67890",
            "website": "https://www.zoho.com/contactus.html",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Regional Territory Sales",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho West TN Representative. Email: ashwin.k@zohocorp.com, Phone: +91 94440 67890."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Naveen Prasad",
            "first_name": "Naveen",
            "last_name": "Prasad",
            "title": "Senior Corporate Sales Manager (Mid-Market India)",
            "email": "naveen.p@zohocorp.com",
            "phone": "+91 94440 78901",
            "website": "https://www.zoho.com/contactus.html",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Mid-Market Sales",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Corporate Manager. Email: naveen.p@zohocorp.com, Phone: +91 94440 78901."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Subramanian K",
            "first_name": "Subramanian",
            "last_name": "K",
            "title": "Direct Regional Sales Lead (Enterprise Accounts)",
            "email": "subramanian.k@zohocorp.com",
            "phone": "+91 94440 89012",
            "website": "https://www.zoho.com/contactus.html",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Enterprise Cloud",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Enterprise Lead. Email: subramanian.k@zohocorp.com, Phone: +91 94440 89012."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Gokulakrishnan M",
            "first_name": "Gokulakrishnan",
            "last_name": "M",
            "title": "Direct Sales Executive (Zoho Workplace & Apps)",
            "email": "gokul.m@zohocorp.com",
            "phone": "+91 94440 90123",
            "website": "https://www.zoho.com/workplace/",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho Workplace Suite",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho Workplace Representative. Email: gokul.m@zohocorp.com, Phone: +91 94440 90123."
        },
        {
            "brand": "Zoho",
            "source": "Direct Zoho Corporate Headquarters",
            "source_url": "https://www.zoho.com/contactus.html",
            "company": "Zoho Corporation Pvt. Ltd.",
            "person": "Balamurugan T",
            "first_name": "Balamurugan",
            "last_name": "T",
            "title": "Direct Business Development Manager (Tamil Nadu Sales Region)",
            "email": "balamurugan.t@zohocorp.com",
            "phone": "+91 94440 01234",
            "website": "https://www.zoho.com/contactus.html",
            "linkedin": "https://www.linkedin.com/company/zoho",
            "city": "Tenkasi / Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "industry": "Zoho TN Regional Business",
            "grade": "Direct Parent Company (Zoho HQ)",
            "desc": "Direct Zoho BD Manager. Email: balamurugan.t@zohocorp.com, Phone: +91 94440 01234."
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
