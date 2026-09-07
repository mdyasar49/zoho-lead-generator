"""
Configuration package for unified Data Scraping framework.
"""

from .settings import settings
from .schemas import STANDARD_HEADERS, ZOHO_CRM_HEADERS, create_standard_lead
from .constants import USER_AGENTS, DEFAULT_KEYWORDS, DEFAULT_LOCATIONS

__all__ = [
    "settings",
    "STANDARD_HEADERS",
    "ZOHO_CRM_HEADERS",
    "create_standard_lead",
    "USER_AGENTS",
    "DEFAULT_KEYWORDS",
    "DEFAULT_LOCATIONS",
]
