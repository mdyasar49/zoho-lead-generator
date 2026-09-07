"""
Core framework package providing browser automation, verification, exporting, and base scraper abstractions.
"""

from .logger import setup_logger, get_logger
from .browser import BrowserManager
from .verifier import LeadVerifier
from .exporter import DataExporter
from .base_scraper import BaseScraper

__all__ = [
    "setup_logger",
    "get_logger",
    "BrowserManager",
    "LeadVerifier",
    "DataExporter",
    "BaseScraper",
]
