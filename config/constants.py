"""
Central Constants and Defaults for Data Scraping Framework.
Modifications here apply globally across all platform scrapers.
"""

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

DEFAULT_LOCATIONS = [
    "Australia",
    "Sydney",
    "Melbourne",
    "Brisbane",
    "Perth",
    "India",
    "Bangalore",
    "Chennai",
    "Mumbai",
    "Hyderabad",
    "United States",
    "United Kingdom"
]

DEFAULT_KEYWORDS = [
    "Software Development",
    "Web Development",
    "Python Developer",
    "React Developer",
    "ERP Implementation",
    "Odoo Partner",
    "Zoho CRM Consultant",
    "Digital Transformation",
    "Cloud Services",
    "AI Automation",
    "coming soon",
    "launching soon",
    "new launch",
    "grand opening"
]

DEFAULT_INDUSTRIES = [
    "IT / Software",
    "ITES / BPO",
    "ICT",
    "Healthcare",
    "Manufacturing",
    "Education",
    "Real Estate",
    "Retail / E-commerce",
    "Consulting",
    "Wholesale & Distribution",
    "Professional Services",
    "Accounting Firms"
]

PLATFORM_URLS = {
    "upwork": "https://www.upwork.com/nx/search/jobs/",
    "freelancer": "https://www.freelancer.com/jobs",
    "peopleperhour": "https://www.peopleperhour.com/freelance-jobs",
    "clutch": "https://clutch.co/developers",
    "designrush": "https://www.designrush.com/agency/software-development",
    "odoo_partners": "https://www.odoo.com/partners",
    "zoho_partners": "https://www.zoho.com/partners/find-partner.html",
    "linkedin": "https://www.linkedin.com/jobs/search",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "twitter": "https://twitter.com",
    "youtube": "https://www.youtube.com",
    "pinterest": "https://www.pinterest.com"
}
