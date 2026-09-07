"""
Standard Lead Data Schemas & Validation Contracts.
Ensures every scraper produces identical, CRM-ready standardized lead dictionaries.
"""

from datetime import datetime
from typing import Dict, Any, Optional

# Standard 21 CRM Headers
STANDARD_HEADERS = [
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

# Extended 31 Enterprise Zoho CRM Headers
ZOHO_CRM_HEADERS = [
    "Scraped Date",
    "Post Date / Posted Date",
    "Post Link / Direct Post URL",
    "Page Link / Profile Page URL",
    "Source Platform",
    "Search Query / Keyword Used",
    "Extracted Post Title / Headline",
    "Cleaned Post Content / Job Description",
    "Business / Profile Name",
    "Author Name",
    "Profile / Username",
    "Designation / Role",
    "Corporate Domain Name",
    "Corporate Website URL",
    "Primary Work Email",
    "Secondary / Alternate Email",
    "Direct Phone / Mobile",
    "Office / Landline Phone",
    "WhatsApp Number / Direct Chat Link",
    "Telegram Handle / URL",
    "LinkedIn Profile URL",
    "Instagram Profile URL",
    "Facebook Profile URL",
    "Twitter / X Profile URL",
    "Primary City",
    "State / Province",
    "Target Country",
    "Matched Industry / Category",
    "Verification Status (Email MX & Phone Valid)",
    "Confidence Score",
    "Action / Lead Status"
]


def create_standard_lead(
    company_name: str = "",
    lead_source: str = "Web Scraping",
    source_url: str = "",
    contact_person: str = "",
    first_name: str = "",
    last_name: str = "",
    job_title: str = "",
    email: str = "",
    phone: str = "",
    website_url: str = "",
    social_url: str = "",
    city: str = "",
    state: str = "",
    country: str = "Australia",
    industry: str = "IT / Software",
    partner_grade: str = "Standard",
    lead_status: str = "New Lead",
    call_status: str = "Not Contacted",
    follow_up_notes: str = "",
    description: str = "",
    extra_fields: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Factory helper to generate a standardized lead item adhering strictly to the CRM schema.
    """
    if contact_person and not first_name:
        parts = contact_person.strip().split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""
    elif first_name and not contact_person:
        contact_person = f"{first_name} {last_name}".strip()

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lead = {
        "Scraped Date": now_str,
        "Lead Source": lead_source,
        "Scraped Website Source URL": source_url,
        "Company Name": company_name,
        "Contact Person": contact_person,
        "First Name": first_name,
        "Last Name": last_name,
        "Job Title": job_title,
        "Work Email": email,
        "Phone Number": phone,
        "Company Website URL": website_url,
        "LinkedIn / Social Profile URL": social_url,
        "City": city,
        "State": state,
        "Country": country,
        "Industry / Module Focus": industry,
        "Partner Grade": partner_grade,
        "Lead Status": lead_status,
        "Call Status": call_status,
        "Follow Up Notes": follow_up_notes,
        "Description": description
    }

    if extra_fields:
        lead.update(extra_fields)

    return lead
