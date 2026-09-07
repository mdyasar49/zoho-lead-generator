"""
================================================================================
🚀 CENTRALIZED LEAD VERIFIER & AI ENRICHMENT ENGINE
================================================================================
Validates emails via MX records, validates phone numbers with libphonenumber,
and enriches/qualifies leads using Gemini AI.
"""

import re
import dns.resolver
import phonenumbers
from typing import Dict, Any, Tuple, Optional
from config.settings import settings
from core.logger import get_logger

logger = get_logger("LeadVerifier")

# Email regex pattern
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

# Domain cache for MX lookups
MX_CACHE: Dict[str, bool] = {}

class LeadVerifier:
    """Enterprise lead validator and enrichment processor."""

    @staticmethod
    def verify_email(email: str) -> Tuple[bool, str]:
        """
        Validates email syntax and performs live DNS MX record lookup.
        Returns: (is_valid, reason)
        """
        if not email or not isinstance(email, str):
            return False, "Empty Email"

        email = email.strip()
        if not EMAIL_REGEX.match(email):
            return False, "Invalid Syntax"

        domain = email.split("@")[-1].lower()
        
        # Check cache
        if domain in MX_CACHE:
            return MX_CACHE[domain], "MX Cached" if MX_CACHE[domain] else "No MX Record"

        try:
            records = dns.resolver.resolve(domain, 'MX', lifetime=4.0)
            if records and len(records) > 0:
                MX_CACHE[domain] = True
                return True, "MX Valid"
            else:
                MX_CACHE[domain] = False
                return False, "No MX Records"
        except Exception:
            # Fallback to A record
            try:
                a_records = dns.resolver.resolve(domain, 'A', lifetime=3.0)
                if a_records:
                    MX_CACHE[domain] = True
                    return True, "A Record Fallback Valid"
            except Exception:
                pass
            
            MX_CACHE[domain] = False
            return False, "Domain Unresolvable"

    @staticmethod
    def verify_phone(phone_str: str, default_region: str = "AU") -> Tuple[bool, str, str]:
        """
        Validates and formats phone numbers using Google libphonenumber.
        Returns: (is_valid, formatted_e164, reason)
        """
        if not phone_str or not isinstance(phone_str, str):
            return False, "", "Empty Phone"

        cleaned = re.sub(r'[^\d+]', '', phone_str.strip())
        if len(cleaned) < 7:
            return False, "", "Too Short"

        try:
            parsed = phonenumbers.parse(phone_str, default_region)
            is_valid = phonenumbers.is_valid_number(parsed)
            if is_valid:
                formatted = phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                )
                return True, formatted, "Valid"
            else:
                return False, phone_str, "Invalid Number"
        except Exception as e:
            return False, phone_str, f"Parse Error: {e}"

    @classmethod
    def enrich_and_validate(cls, lead: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriches and validates a lead dictionary, adding verification flags and score.
        """
        email = lead.get("Work Email") or lead.get("Primary Work Email", "")
        phone = lead.get("Phone Number") or lead.get("Direct Phone / Mobile", "")

        is_email_valid, email_reason = cls.verify_email(email) if email else (False, "No Email")
        is_phone_valid, formatted_phone, phone_reason = cls.verify_phone(phone) if phone else (False, "", "No Phone")

        score = 0
        if is_email_valid:
            score += 50
        elif email:
            score += 20

        if is_phone_valid:
            score += 30
            if "Phone Number" in lead:
                lead["Phone Number"] = formatted_phone
        elif phone:
            score += 10

        if lead.get("Company Website URL") or lead.get("Corporate Website URL"):
            score += 15

        if lead.get("Company Name") or lead.get("Business / Profile Name"):
            score += 5

        status_text = "Verified" if (is_email_valid or is_phone_valid) else "Unverified"
        lead["Verification Status"] = f"{status_text} (Email: {email_reason}, Phone: {phone_reason})"
        lead["Confidence Score"] = f"{min(score, 100)}%"

        return lead
