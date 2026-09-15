"""
Centralized Logger for all scrapers.
Provides consistent formatting, timestamping, console output, and daily rotating log files.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config.settings import settings

def setup_logger(name: str = "ScraperEngine", log_level: int = logging.INFO) -> logging.Logger:
    """Configures and returns a standardized logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if settings.DEBUG else log_level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Log format
    log_format = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # File Handler
    try:
        settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        log_file = settings.LOGS_DIR / f"{name.lower().replace(' ', '_')}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not initialize file logger: {e}")

    return logger

def get_logger(name: str = "ScraperEngine") -> logging.Logger:
    """Convenience getter for existing logger."""
    return logging.getLogger(name) if logging.getLogger(name).handlers else setup_logger(name)
