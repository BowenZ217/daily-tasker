#!/usr/bin/env python3
"""
daily_tasker.config
-------------------

Config loading interface for site definitions and account credentials.
"""

from .adapter import AccountsAdapter, ConfigAdapter
from .loader import load_site_accounts, load_site_config

__all__ = [
    "AccountsAdapter",
    "ConfigAdapter",
    "load_site_config",
    "load_site_accounts",
]
