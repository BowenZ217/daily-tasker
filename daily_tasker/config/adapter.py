#!/usr/bin/env python3
"""
daily_tasker.config.adapter
---------------------------

"""

import logging
from dataclasses import fields, is_dataclass
from typing import TYPE_CHECKING, Any, TypeVar

from daily_tasker.config.models import (
    Account,
    DebugConfig,
    RequesterConfig,
    SiteConfig,
    TaskerConfig,
)

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

DataclassT = TypeVar("DataclassT", bound="DataclassInstance")
logger = logging.getLogger(__name__)


class AccountsAdapter:
    def __init__(self, raw_accounts: dict[str, Any]) -> None:
        """ """
        self._raw = raw_accounts
        self._cache: dict[str, dict[str, Account]] = {}

    def parse(self) -> dict[str, dict[str, Account]]:
        """
        Parse *all* sites/accounts once and cache them.
        """
        if self._cache:
            return self._cache

        for site_name, site_block in self._raw.items():
            accounts_block = site_block.get("accounts", {})
            parsed: dict[str, Account] = {}
            for user_key, data in accounts_block.items():
                acct = Account(
                    username=data.get("username"),
                    password=data.get("password"),
                    raw_cookies=data.get("cookies", {}),
                )
                parsed[user_key] = acct
            self._cache[site_name] = parsed

        return self._cache

    def get_accounts(self, site: str) -> dict[str, Account]:
        """
        All accounts for a given site.
        """
        all_sites = self.parse()
        return all_sites.get(site, {})

    def get_account(self, site: str, user: str) -> Account:
        """
        Single Account object for site/user-KeyError if not found.
        """
        return self.get_accounts(site)[user]


class ConfigAdapter:
    def __init__(self, raw_config: dict[str, Any]) -> None:
        """ """
        self._raw = raw_config

    def _filter_dataclass_args(
        self, cls: type[DataclassT], config: dict[str, Any]
    ) -> dict[str, Any]:
        if not is_dataclass(cls):
            raise TypeError(f"{cls} is not a dataclass")
        valid_keys = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in config.items() if k in valid_keys}
        extra_keys = set(config) - valid_keys
        if extra_keys:
            logger.warning(
                f"Ignoring unknown keys for {cls.__name__}: {', '.join(extra_keys)}"
            )
        return filtered

    def get_requester_config(self) -> RequesterConfig:
        req = self._raw.get("global", {}).get("requests", {})
        filtered = self._filter_dataclass_args(RequesterConfig, req)
        return RequesterConfig(**filtered)

    def get_tasker_config(self) -> TaskerConfig:
        rt = self._raw.get("global", {}).get("runtime", {})
        filtered = self._filter_dataclass_args(TaskerConfig, rt)
        return TaskerConfig(**filtered)

    def get_debug_config(self) -> DebugConfig:
        dbg = self._raw.get("global", {}).get("debug", {})
        filtered = self._filter_dataclass_args(DebugConfig, dbg)
        return DebugConfig(**filtered)

    def get_site_config(self, site: str) -> SiteConfig:
        site_config = self._raw.get("sites", {}).get(site, {})
        if not isinstance(site_config, dict):
            raise TypeError(
                f"Expected dict for site config '{site}', "
                f"got {type(site_config).__name__}"
            )
        return SiteConfig(**site_config)
