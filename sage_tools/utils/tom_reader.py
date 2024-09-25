"""
toml_reader
~~~~~~~~~~~

This module contains a singleton class for reading and parsing a TOML configuration
file.
The module uses `tomllib` to parse the TOML file and provides a method to retrieve
configuration values from it.
"""

import logging
from typing import Any, Dict, Optional

import tomllib

logger = logging.getLogger(__name__)


class TomlConfigParser:
    """A singleton class for parsing TOML configuration files and retrieving
    configuration values."""

    _shared_state: Dict[str, Any] = {}

    def __init__(self, config_file_path: str):
        """Initialize the TomlConfigParser instance."""
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self._config_file_path = config_file_path
            self.config_data = self.__load_config_data()

    def __load_config_data(self) -> Dict[str, Any]:
        """Load and parse the TOML configuration file."""
        try:
            with open(self._config_file_path, "rb") as settings_file:
                conf = tomllib.load(settings_file)
        except FileNotFoundError as err:
            err_msg = f"The `{self._config_file_path}` file does not exist!"
            raise FileNotFoundError(err_msg) from err
        except tomllib.TOMLDecodeError as err:
            err_msg = f"The `{self._config_file_path}` file contains invalid TOML syntax! Error: {err}"  # pylint: disable = c0301
            raise ValueError(err_msg) from err
        return conf

    def get_value(self, category: str, key: Optional[str] = None, default=None) -> Any:
        """Retrieve a specific value from the TOML data."""
        if "." in category:
            parent_conf, child_conf = category.split(".")
            parent_config = self.config_data.get(parent_conf)

            if parent_config is None:
                raise AssertionError(
                    f"No configuration found for category '{parent_conf}'"
                )

            conf = parent_config.get(child_conf)
        else:
            conf = self.config_data.get(category)
            if conf is None:
                raise AssertionError(
                    f"No configuration found for category '{category}'"
                )

        if key:
            conf = conf.get(key, default)
            if conf is None:
                raise AssertionError(
                    f"No configuration found for key '{key}' in category '{category}'"
                )

        return conf
