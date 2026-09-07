"""
Scrapers registry and loader for all data scraping modules.
"""

from .b2b import ClutchScraper, DesignRushScraper, OdooPartnerScraper, ZohoPartnerScraper
from .freelance import UpworkScraper, FreelancerScraper, PeoplePerHourScraper
from .social import (
    LinkedInScraper,
    FacebookScraper,
    InstagramScraper,
    TwitterScraper,
    YouTubeScraper,
    PinterestScraper,
    SerperSocialScraper
)

SCRAPERS_REGISTRY = {
    # B2B
    "clutch": ClutchScraper,
    "designrush": DesignRushScraper,
    "odoo_partners": OdooPartnerScraper,
    "zoho_partners": ZohoPartnerScraper,
    
    # Freelance
    "upwork": UpworkScraper,
    "freelancer": FreelancerScraper,
    "peopleperhour": PeoplePerHourScraper,
    
    # Social
    "linkedin": LinkedInScraper,
    "facebook": FacebookScraper,
    "instagram": InstagramScraper,
    "twitter": TwitterScraper,
    "youtube": YouTubeScraper,
    "pinterest": PinterestScraper,
    "serper_social": SerperSocialScraper
}

__all__ = [
    "SCRAPERS_REGISTRY",
    "ClutchScraper",
    "DesignRushScraper",
    "OdooPartnerScraper",
    "ZohoPartnerScraper",
    "UpworkScraper",
    "FreelancerScraper",
    "PeoplePerHourScraper",
    "LinkedInScraper",
    "FacebookScraper",
    "InstagramScraper",
    "TwitterScraper",
    "YouTubeScraper",
    "PinterestScraper",
    "SerperSocialScraper"
]
