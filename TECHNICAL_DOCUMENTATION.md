# 📑 Technical Documentation: `zoho-lead-generator`

## 📌 Project Overview
**`zoho-lead-generator`** is an automated Technographic Hunter and B2B Prospecting engine built to discover companies utilizing the Zoho Ecosystem (Zoho CRM, Zoho Books, Zoho One, Deluge) across Australia and India.

---

## ⚡ How to Run the Project (Execution Commands)

### 1. Prerequisites
- Python 3.10+
- Zoho CRM Deluge Scripting Access / API v2 Token
- Install dependencies:
  ```bash
  pip install requests beautifulsoup4 gspread google-auth
  ```

### 2. Manual Execution Command
* **Python Direct Extractor**:
  ```bash
  python Social-Media-Data-Scraping/upload_all_sheets_direct_to_zoho.py
  ```
* **Deluge Scheduled Script (Inside Zoho CRM)**:
  Executes `ZOHO_CRM_DELUGE_SCHEDULED_FUNCTION_CLEAN.deluge` inside Zoho CRM Function Manager.

### 3. Automated Schedule Setup
* **Zoho CRM Native Scheduler**: Set to trigger every **24 Hours at 08:00 AM**.
* **Windows Task Scheduler**:
  ```powershell
  schtasks /create /tn "ZohoLeadGeneratorCron" /tr "python d:\infonix\Social-Media-Data-Scraping\upload_all_sheets_direct_to_zoho.py" /sc daily /st 09:00 /f /rl HIGHEST
  ```

---

## ⏱️ Execution Frequency (Evlo Time ku Once Run Aagum)
* **Schedule Interval**: **Daily at 08:00 AM & 09:00 AM** (Runs once every 24 hours).
* **Real-Time Zoho Flow Integration**: Listens continuously via webhooks for new Google Sheets row insertions.

---

## 🔑 Exact Scraping Keywords & Search Patterns Used

### 1. Product & Ecosystem Keywords
* `Zoho CRM`
* `Zoho One`
* `Zoho Books`
* `Zoho Creator`
* `Zoho Desk`
* `Deluge Scripting`
* `Zoho Flow`

### 2. Search Dorks & Geographic Queries
* `"Zoho Advanced Partner" Sydney`
* `"Zoho Authorized Partner" Melbourne`
* `"Zoho CRM migration"`
* `"Zoho integration partner" India`
* `site:zoho.com/partners "Australia"`
* `site:zoho.com/partners "India"`

### 3. Target Industry Sectors
* `IT / Software & Cloud Services`
* `Professional Services & Consulting`
* `Manufacturing & Wholesale Distribution`
* `Accounting & Financial Services`

---

## 📊 Scraped Data Schema & Extracted Fields
* **Lead Source**: `Zoho Partner Directory` / `Google Search` / `Zoho Sheet`
* **Company**: Enterprise Legal Name
* **First Name & Last Name**: Contact Person
* **Email**: Validated Corporate Email
* **Phone Number**: Formatted (`+61 ...` / `+91 ...`)
* **Mobile Number**: Direct cell number
* **Industry**: Target Sector
* **Rating**: Lead Tier (`Acquired`, `Attempted Contact`, `Qualified`)
* **Sync Status**: `Pushed to Zoho CRM API v2`
