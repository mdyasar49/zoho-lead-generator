"""
================================================================================
🚀 CENTRALIZED RESILIENT ANTI-DETECTION BROWSER FACTORY
================================================================================
Modifying browser flags, user agents, proxy, or stealth features here
instantly upgrades all platform scrapers across the entire project!
"""

import random
import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import settings
from config.constants import USER_AGENTS
from core.logger import get_logger

logger = get_logger("BrowserManager")

class BrowserManager:
    """Enterprise-grade Chrome WebDriver manager with anti-bot evasion."""

    @staticmethod
    def get_chrome_options(
        headless: Optional[bool] = None,
        custom_user_agent: Optional[str] = None,
        use_profile: bool = False
    ) -> Options:
        """Constructs standardized stealth ChromeOptions."""
        options = Options()

        is_headless = settings.HEADLESS if headless is None else headless
        if is_headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        
        # Anti-Detection & Sandbox Arguments
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")

        # Exclude automation switches
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Performance & Network optimizations
        options.add_argument("--disable-notifications")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")

        # Proxy support if defined
        if settings.PROXY_URL:
            options.add_argument(f"--proxy-server={settings.PROXY_URL}")

        # User Agent configuration
        ua = custom_user_agent or random.choice(USER_AGENTS)
        options.add_argument(f"user-agent={ua}")

        # Optional Profile persistence
        if use_profile and settings.USER_DATA_DIR:
            options.add_argument(f"--user-data-dir={settings.USER_DATA_DIR}")

        # Preferences (disable autofill/passwords popups)
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_experimental_option("prefs", prefs)

        return options

    @classmethod
    def create_driver(
        cls,
        headless: Optional[bool] = None,
        custom_user_agent: Optional[str] = None,
        use_profile: bool = False
    ) -> webdriver.Chrome:
        """Initializes and returns a configured Chrome WebDriver with stealth script injection."""
        options = cls.get_chrome_options(
            headless=headless,
            custom_user_agent=custom_user_agent,
            use_profile=use_profile
        )

        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            logger.warning(f"ChromeDriverManager install failed, attempting default ChromeDriver: {e}")
            driver = webdriver.Chrome(options=options)

        # Apply stealth overrides via CDP
        try:
            driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                        Object.defineProperty(navigator, 'plugins', {
                            get: () => [1, 2, 3, 4, 5]
                        });
                        Object.defineProperty(navigator, 'languages', {
                            get: () => ['en-US', 'en']
                        });
                        window.chrome = {
                            runtime: {}
                        };
                    """
                }
            )
        except Exception as e:
            logger.debug(f"CDP stealth script injection note: {e}")

        driver.set_page_load_timeout(settings.BROWSER_TIMEOUT)
        logger.info(f"Initialized Chrome WebDriver (Headless={settings.HEADLESS if headless is None else headless})")
        return driver

    @staticmethod
    def safe_quit(driver: Optional[webdriver.Chrome]):
        """Safely quits and cleans up the browser instance."""
        if driver:
            try:
                driver.quit()
                logger.info("Chrome WebDriver closed successfully.")
            except Exception as e:
                logger.debug(f"Error while closing driver: {e}")
