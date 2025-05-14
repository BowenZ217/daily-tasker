#!/usr/bin/env python3
"""
daily_tasker.utils.constants
----------------------------

Constants and default paths used throughout the DailyTasker project.
"""

from importlib.resources import files
from pathlib import Path

from platformdirs import user_config_dir

# -----------------------------------------------------------------------------
# Application identity
# -----------------------------------------------------------------------------
PACKAGE_NAME = "daily_tasker"  # Python package name
APP_NAME = "DailyTasker"  # Display name
APP_DIR_NAME = "daily_tasker"  # Directory name for platformdirs
LOGGER_NAME = PACKAGE_NAME  # Root logger name


# -----------------------------------------------------------------------------
# Base directories
# -----------------------------------------------------------------------------
# Base config directory (e.g. ~/AppData/Local/daily_tasker/)
BASE_CONFIG_DIR = Path(user_config_dir(APP_DIR_NAME, appauthor=False))

# Subdirectories under BASE_CONFIG_DIR
DATA_DIR = BASE_CONFIG_DIR / "data"
CONFIG_DIR = BASE_CONFIG_DIR / "config"

# -----------------------------------------------------------------------------
# Default file paths
# -----------------------------------------------------------------------------
STATE_FILE = CONFIG_DIR / "state.json"
SITE_CONFIG_FILE = CONFIG_DIR / "site_config.json"
SITE_ACCOUNTS_FILE = CONFIG_DIR / "site_accounts.json"
DEFAULT_USER_DATA_DIR = DATA_DIR / "browser_data"


# -----------------------------------------------------------------------------
# Default preferences & headers
# -----------------------------------------------------------------------------
DEFAULT_USER_PROFILE_NAME = "Profile_1"

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
)
DEFAULT_HEADERS = {"User-Agent": DEFAULT_USER_AGENT}

DEFAULT_ACCEPT = (
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
)

DEFAULT_USER_HEADERS = {
    "Accept": DEFAULT_ACCEPT,
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en,zh;q=0.9,zh-CN;q=0.8",
    "User-Agent": DEFAULT_USER_AGENT,
    "Connection": "keep-alive",
}

# -----------------------------------------------------------------------------
# Embedded resources (via importlib.resources)
# -----------------------------------------------------------------------------
BASE_ACCOUNTS_PATH = files("daily_tasker.resources.templates").joinpath(
    "site_accounts.toml"
)
BASE_CONFIG_PATH = files("daily_tasker.resources.templates").joinpath(
    "site_config.yaml"
)

DEFAULT_SETTINGS_PATHS = [
    BASE_ACCOUNTS_PATH,
    BASE_CONFIG_PATH,
]
