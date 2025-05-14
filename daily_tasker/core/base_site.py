#!/usr/bin/env python3
"""
daily_tasker.core.base_site
---------------------------

Defines the abstract base class for all site implementations.
Each instance handles one account and a custom sequence of tasks.
"""

import abc
import logging
from collections.abc import Callable
from typing import Any

from daily_tasker.utils.cookies import resolve_cookies


class BaseSite(abc.ABC):
    def __init__(
        self,
        site_conf: dict[str, Any],
        account_conf: dict[str, Any],
    ) -> None:
        """
        Initialize a site instance for a specific account.

        :param site_conf: The configuration dictionary for the site.
        :param account_conf: The configuration dictionary for the account.
        """
        self._site_conf = site_conf
        self._account_conf = account_conf
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        try:
            self._cookies = resolve_cookies(account_conf.get("cookies", {}))
        except Exception as e:
            self._cookies = {}
            self.logger.warning("Failed to parse cookies: %s", e)

        self.task_sequence: list[Callable[[], None]] = []
        self.build_task_sequence()

    @abc.abstractmethod
    def build_task_sequence(self) -> None:
        """
        Define the ordered list of tasks to be executed for this account.
        Subclasses must implement this method to populate `self.task_sequence`.
        """
        ...

    def run_all_tasks(self) -> None:
        """
        Run all tasks defined in the task sequence for this account.
        """
        for task in self.task_sequence:
            task()
        return

    @property
    def site_conf(self) -> dict[str, Any]:
        """Access the site configuration."""
        return self._site_conf

    @property
    def account_conf(self) -> dict[str, Any]:
        """Access the account configuration."""
        return self._account_conf

    @property
    def username(self) -> str:
        """Get the username from the account config."""
        return self._account_conf.get("username", "") or ""

    @property
    def password(self) -> str:
        """Get the password from the account config."""
        return self._account_conf.get("password", "") or ""

    @property
    def cookies(self) -> dict[str, str]:
        """Get the cookies from the account config."""
        return self._cookies
