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

from daily_tasker.config.models import (
    Account,
    RequesterConfig,
    SiteConfig,
)


class BaseSite(abc.ABC):
    def __init__(
        self,
        request_conf: RequesterConfig,
        account_conf: Account,
        site_conf: SiteConfig,
        use_browser: bool = False,
    ) -> None:
        """
        Initialize a site instance for a specific account.

        :param request_conf: The configuration dict for the request.
        :param account_conf: The configuration dict for the account.
        :param site_conf: The configuration dict for the site.
        """
        self._site_conf = site_conf
        self._request_conf = request_conf
        self._account_conf = account_conf
        self.use_browser = use_browser
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

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
    def site_conf(self) -> SiteConfig:
        """Access the site configuration."""
        return self._site_conf

    @property
    def request_conf(self) -> RequesterConfig:
        """Access the request configuration."""
        return self._request_conf

    @property
    def account_conf(self) -> Account:
        """Access the account configuration."""
        return self._account_conf

    @property
    def enabled(self) -> bool:
        return self._site_conf.enabled

    @property
    def username(self) -> str:
        """Get the username from the account config."""
        return self._account_conf.username

    @property
    def password(self) -> str:
        """Get the password from the account config."""
        return self._account_conf.password

    @property
    def cookies(self) -> dict[str, str]:
        """Get the cookies from the account config."""
        return self._account_conf.cookies
