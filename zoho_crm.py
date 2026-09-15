"""
================================================================================
🚀 ZOHO CRM DIRECT API CONNECTOR & BATCH UPSERTER (ODOO & ZOHO SALES LEADS)
================================================================================
"""

import os
import sys
import json
import requests
from typing import List, Dict, Any, Optional

DEFAULT_ZOHO_CLIENT_ID = "1000.I8BXR1U9XEX0TGSSBBS969PUAQDDCO"
DEFAULT_ZOHO_CLIENT_SECRET = "f0b12ded0b82b34eca1aa52f3a4e688ac43603755b"
DEFAULT_ZOHO_REFRESH_TOKEN = "1000.fb5b161d68abd14ef17be0b078337e7d.b7d8d9d85d96eaa03498881c09a5f294"
DEFAULT_ZOHO_ACCOUNTS_URL = "https://accounts.zoho.in/oauth/v2/token"
DEFAULT_ZOHO_API_URL = "https://www.zohoapis.in/crm/v2/Leads"

def get_zoho_access_token() -> Optional[str]:
    client_id = os.getenv("ZOHO_CLIENT_ID", DEFAULT_ZOHO_CLIENT_ID)
    client_secret = os.getenv("ZOHO_CLIENT_SECRET", DEFAULT_ZOHO_CLIENT_SECRET)
    refresh_token = os.getenv("ZOHO_REFRESH_TOKEN", DEFAULT_ZOHO_REFRESH_TOKEN)

    # Check local self_client.json if exists
    for p in ["self_client.json", "../infogenx-twilio-dialer/self_client.json", "../self_client.json"]:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    c = json.load(f)
                    client_id = c.get("client_id", client_id)
                    client_secret = c.get("client_secret", client_secret)
                    refresh_token = c.get("refresh_token", refresh_token)
                break
            except Exception:
                pass

    try:
        params = {
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token"
        }
        res = requests.post(DEFAULT_ZOHO_ACCOUNTS_URL, params=params, timeout=15)
        data = res.json()
        return data.get("access_token")
    except Exception as e:
        print(f"[-] Zoho OAuth Token Error: {e}")
        return None

def upload_leads_to_zoho_crm(leads: List[Dict[str, Any]], lead_source: str = "Sales Partner Lead Generator") -> int:
    token = get_zoho_access_token()
    if not token:
        print("[-] Zoho CRM upload skipped: Auth token unavailable.")
        return 0

    headers = {
        "Authorization": f"Zoho-oauthtoken {token}",
        "Content-Type": "application/json"
    }

    crm_batch = []
    for lead in leads:
        email = (lead.get("Work Email") or lead.get("Email") or "").strip()
        phone = (lead.get("Phone Number") or lead.get("Phone") or "").strip()
        last_name = lead.get("Last Name") or lead.get("Contact Person") or lead.get("Company Name") or "Partner Lead"
        first_name = lead.get("First Name") or ""
        company = lead.get("Company Name") or "Technology Enterprise"
        designation = lead.get("Job Title") or lead.get("Designation") or "Executive"
        city = lead.get("City") or ""
        state = lead.get("State") or ""
        country = lead.get("Country") or "India"
        source = lead.get("Lead Source") or lead_source
        notes = lead.get("Follow Up Notes") or lead.get("Description") or ""

        if not email and not phone:
            continue

        crm_lead = {
            "Last_Name": last_name,
            "Company": company,
            "Lead_Source": source
        }
        if first_name:
            crm_lead["First_Name"] = first_name
        if email:
            crm_lead["Email"] = email
        if phone:
            crm_lead["Phone"] = phone
            crm_lead["Mobile"] = phone
        if designation:
            crm_lead["Designation"] = designation
        if city:
            crm_lead["City"] = city
        if state:
            crm_lead["State"] = state
        if country:
            crm_lead["Country"] = country
        if notes:
            crm_lead["Description"] = notes[:1000]

        crm_batch.append(crm_lead)

    if not crm_batch:
        return 0

    uploaded = 0
    for i in range(0, len(crm_batch), 50):
        chunk = crm_batch[i:i+50]
        payload = {"data": chunk, "duplicate_check_fields": ["Email"]}
        try:
            res = requests.post(f"{DEFAULT_ZOHO_API_URL}/upsert", json=payload, headers=headers, timeout=20)
            if res.status_code in [200, 201, 202]:
                data = res.json().get("data", [])
                for it in data:
                    if str(it.get("status") or it.get("code")).lower() in ["success", "created"]:
                        uploaded += 1
        except Exception as e:
            print(f"[-] Zoho Post Batch Error: {e}")

    print(f"[✓] Uploaded {uploaded} / {len(crm_batch)} leads directly to Zoho CRM API!")
    return uploaded
