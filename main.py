"""
================================================================================
🚀 ENTERPRISE UNIFIED SCRAPER RUNNER & CLI ORCHESTRATOR
================================================================================
Usage Examples:
    # Run a specific scraper:
    python main.py --scraper upwork
    python main.py --scraper odoo_partners --limit 10

    # Run a category of scrapers:
    python main.py --category b2b
    python main.py --category freelance
    python main.py --category social

    # Run all scrapers:
    python main.py --all

    # Interactive menu:
    python main.py --interactive
"""

import sys
import argparse
from typing import List
from config.settings import settings
from config.schemas import STANDARD_HEADERS
from scrapers import SCRAPERS_REGISTRY
from core.logger import setup_logger

logger = setup_logger("MasterRunner")

CATEGORY_MAP = {
    "b2b": ["clutch", "designrush", "odoo_partners", "zoho_partners"],
    "freelance": ["upwork", "freelancer", "peopleperhour"],
    "social": ["linkedin", "facebook", "instagram", "twitter", "youtube", "pinterest", "serper_social"]
}

def print_banner():
    print(r"""
================================================================================
 ⚡ ENTERPRISE UNIFIED DATA SCRAPING SUITE (v2.0)
 ⚡ Modular Single-Source-of-Truth Architecture
================================================================================
    """)

def run_scraper_by_name(name: str, limit: int = 50, headless: bool = True):
    """Instantiates and executes a single registered scraper."""
    scraper_cls = SCRAPERS_REGISTRY.get(name)
    if not scraper_cls:
        logger.error(f"Unknown scraper: '{name}'. Available: {list(SCRAPERS_REGISTRY.keys())}")
        return None

    logger.info(f"Initializing scraper: {name}...")
    scraper_instance = scraper_cls(headless=headless)
    result = scraper_instance.run(max_results=limit)
    return result

def run_category(category: str, limit: int = 30, headless: bool = True):
    """Runs all scrapers within a given category."""
    scraper_names = CATEGORY_MAP.get(category.lower())
    if not scraper_names:
        logger.error(f"Unknown category: '{category}'. Choose from: {list(CATEGORY_MAP.keys())}")
        return

    logger.info(f"========== Running Category: {category.upper()} ==========")
    for name in scraper_names:
        run_scraper_by_name(name, limit=limit, headless=headless)

def run_all(limit: int = 25, headless: bool = True):
    """Runs all registered scrapers across all categories."""
    logger.info("========== Running ALL Platform Scrapers ==========")
    for name in SCRAPERS_REGISTRY.keys():
        run_scraper_by_name(name, limit=limit, headless=headless)

def interactive_menu():
    """Interactive CLI menu."""
    print_banner()
    print("Available Scrapers:")
    for idx, name in enumerate(SCRAPERS_REGISTRY.keys(), 1):
        print(f"  [{idx}] {name}")
    print("\nCategories:")
    print("  [B] B2B (Clutch, DesignRush, Odoo, Zoho)")
    print("  [F] Freelance (Upwork, Freelancer, PPH)")
    print("  [S] Social (LinkedIn, FB, IG, X, YT, Pinterest, Serper)")
    print("  [A] Run All Scrapers")
    print("  [Q] Quit")

    choice = input("\nEnter your choice: ").strip().lower()
    if choice == 'q':
        sys.exit(0)
    elif choice == 'a':
        run_all()
    elif choice == 'b':
        run_category("b2b")
    elif choice == 'f':
        run_category("freelance")
    elif choice == 's':
        run_category("social")
    elif choice.isdigit() and 1 <= int(choice) <= len(SCRAPERS_REGISTRY):
        scraper_name = list(SCRAPERS_REGISTRY.keys())[int(choice) - 1]
        run_scraper_by_name(scraper_name)
    else:
        print("Invalid choice.")

def main():
    parser = argparse.ArgumentParser(description="Enterprise Unified Data Scraping Suite")
    parser.add_argument("--scraper", type=str, help=f"Run a specific scraper ({', '.join(SCRAPERS_REGISTRY.keys())})")
    parser.add_argument("--category", type=str, help="Run a category (b2b, freelance, social)")
    parser.add_argument("--all", action="store_true", help="Run all scrapers sequentially")
    parser.add_argument("--limit", type=int, default=30, help="Max leads to scrape per source (default: 30)")
    parser.add_argument("--no-headless", action="store_true", help="Run browser in visible mode (default: headless)")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive menu")

    args = parser.parse_args()
    headless = not args.no_headless

    if args.interactive or (len(sys.argv) == 1):
        interactive_menu()
    elif args.scraper:
        run_scraper_by_name(args.scraper, limit=args.limit, headless=headless)
    elif args.category:
        run_category(args.category, limit=args.limit, headless=headless)
    elif args.all:
        run_all(limit=args.limit, headless=headless)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
