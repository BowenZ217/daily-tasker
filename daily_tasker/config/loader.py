#!/usr/bin/env python3
"""
daily_tasker.config.loader
--------------------------

Provides functions to resolve and load site and account configuration files.

This module supports layered configuration resolution in the following priority:
1. User-specified path via function arguments
2. Local default file in the current working directory (e.g. 'site_config.toml')
3. Globally registered fallback path
"""

import json
import logging
import tomllib
from pathlib import Path
from typing import Any

from daily_tasker.utils.cache import cached_load_config
from daily_tasker.utils.constants import (
    SITE_ACCOUNTS_FILE,
    SITE_CONFIG_FILE,
)

logger = logging.getLogger(__name__)


def resolve_file_path(
    user_path: str | Path | None,
    local_filename: str,
    fallback_path: Path,
) -> Path | None:
    """
    Resolve the file path to use based on a prioritized lookup order.

    Priority:
        1. A user-specified path (if provided and exists)
        2. A file in the current working directory with the given name
        3. A globally registered fallback path

    :param user_path: Optional user-specified file path.
    :param local_filename: File name to check in the current working directory.
    :param fallback_path: Fallback path used if other options are not available.
    :return: A valid Path object if found, otherwise None.
    """
    if user_path:
        path = Path(user_path).expanduser().resolve()
        if path.is_file():
            return path
        logger.warning("[config] Specified file not found: %s", path)

    local_path = Path.cwd() / local_filename
    if local_path.is_file():
        logger.debug("[config] Using local file: %s", local_path)
        return local_path

    if fallback_path.is_file():
        logger.debug("[config] Using fallback file: %s", fallback_path)
        return fallback_path

    logger.warning("[config] No file found at any location for: %s", local_filename)
    return None


def _validate_dict(data: Any, path: Path, format: str) -> dict[str, Any]:
    """
    Validate that the parsed config is a dictionary.

    :param data: The loaded content to validate.
    :param path: Path to the original config file (used for logging).
    :param format: Format name ('json', 'toml', etc.) for log context.
    :return: The original data if valid, otherwise an empty dict.
    """
    if not isinstance(data, dict):
        logger.warning(
            "[config] %s content is not a dictionary: %s",
            format.upper(),
            path,
        )
        return {}
    return data


def _load_by_extension(path: Path) -> dict[str, Any]:
    """
    Load a configuration file by its file extension.

    Supports `.toml` and `.json` formats.

    :param path: Path to the configuration file.
    :return: Parsed configuration as a dictionary.
    :raises ValueError: If the file extension is unsupported.
    """
    ext = path.suffix.lower()
    if ext == ".json":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return _validate_dict(data, path, "json")
    elif ext == ".toml":
        with path.open("rb") as f:
            data = tomllib.load(f)
            return _validate_dict(data, path, "toml")
    else:
        raise ValueError(f"Unsupported config file extension: {ext}")


@cached_load_config
def load_site_config(
    config_path: str | Path | None = None,
) -> dict[str, Any]:
    """
    Load the site configuration from a TOML or JSON file.

    Resolves the configuration path based on user input, local file,
    or global fallback, then loads and parses the file.

    :param config_path: Optional path to a configuration file.
    :return: Parsed site configuration as a dictionary.
    :raises FileNotFoundError: If no configuration file is found.
    :raises ValueError: If the file format is unsupported.
    """
    path = resolve_file_path(
        user_path=config_path,
        local_filename="site_config.toml",
        fallback_path=SITE_CONFIG_FILE,
    )
    if not path:
        raise FileNotFoundError("No site config file found.")

    return _load_by_extension(path)


@cached_load_config
def load_site_accounts(
    accounts_path: str | Path | None = None,
) -> dict[str, Any]:
    """
    Load the site account credentials from a TOML or JSON file.

    Resolves the account file path based on user input, local file,
    or global fallback, then loads and parses the file.

    :param accounts_path: Optional path to an account configuration file.
    :return: Parsed account configuration as a dictionary.
    :raises FileNotFoundError: If no account file is found.
    :raises ValueError: If the file format is unsupported.
    """
    path = resolve_file_path(
        user_path=accounts_path,
        local_filename="site_accounts.toml",
        fallback_path=SITE_ACCOUNTS_FILE,
    )
    if not path:
        raise FileNotFoundError("No site account file found.")

    return _load_by_extension(path)
