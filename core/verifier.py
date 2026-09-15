"""
================================================================================
🚀 CENTRALIZED LEAD VERIFIER & DELIVERABILITY ENGINE
================================================================================
Validates emails via syntax, negative blacklists, and live DNS MX records.
Filters out dead domains, job aggregators, and bouncing email addresses.
Validates phone numbers with Google's libphonenumber.
================================================================================
"""

import os
import sys
import re
from typing import Dict, Any, Tuple, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from lead_verifier import is_email_deliverable, verify_phone_number
from core.logger import get_logger

logger = get_logger("LeadVerifier")

class LeadVerifier:
    """Enterprise lead validator and zero-bounce deliverability engine."""

    @staticmethod
    def verify_email(email: str) -> Tuple[bool, str]:
        """
        Validates email syntax, checks blacklist, job portals, and live DNS MX records.
        Returns: (is_valid, reason)
        """
        if not email or not isinstance(email, str):
            return False, "Empty Email"
        ok, clean_em, reason = is_email_deliverable(email.strip())
        return ok, reason

    @staticmethod
    def verify_phone(phone_str: str, default_region: str = "AU") -> Tuple[bool, str, str]:
        """
        Validates and formats phone numbers using Google libphonenumber.
        Returns: (is_valid, formatted_e164, reason)
        """
        if not phone_str or not isinstance(phone_str, str):
            return False, "", "Empty Phone"
        ok, formatted, ptype, reason = verify_phone_number(phone_str.strip(), default_region)
        return ok, formatted, reason

    @classmethod
    def enrich_and_validate(cls, lead: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriches and validates a lead dictionary, adding verification flags and score.
        """
        email = lead.get("Work Email") or lead.get("Primary Work Email") or lead.get("Email") or ""
        phone = lead.get("Phone Number") or lead.get("Direct Phone / Mobile") or lead.get("Phone") or ""

        is_email_valid, email_reason = cls.verify_email(email) if email else (False, "No Email")
        is_phone_valid, formatted_phone, phone_reason = cls.verify_phone(phone) if phone else (False, "", "No Phone")

        score = 0
        if is_email_valid:
            score += 60
        if is_phone_valid:
            score += 30
            if "Phone Number" in lead:
                lead["Phone Number"] = formatted_phone
            elif "Phone" in lead:
                lead["Phone"] = formatted_phone

        if lead.get("Company Website URL") or lead.get("Corporate Website URL") or lead.get("Website"):
            score += 10

        status_text = "Verified" if is_email_valid else "Unverified"
        lead["Verification Status"] = f"{status_text} (Email: {email_reason}, Phone: {phone_reason})"
        lead["Confidence Score"] = f"{min(score, 100)}%"

        return lead
