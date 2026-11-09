from pathlib import Path
from typing import Any

import yaml


class ConfigLoader:
    """
    ConfigLoader class loads the YAML configuration file of the service (e.g., fetcher_conf.yaml).

    A relative path is searched in the current working directory and, if not found, in the service root directory,
    so the service can be started from any folder.
    """

    # Service root directory: src/mqtt_data_fetcher/config/config_loader.py -> 3 levels up
    PROJECT_ROOT_DIR = Path(__file__).resolve().parents[3]

    @classmethod
    def resolve_path(cls, config_file: str | Path) -> Path:
        """
        Resolve the path of a configuration file
        :param config_file: Absolute path or path relative to the working directory or to the project root
        :return: The path of the existing configuration file
        """

        config_path = Path(config_file)
        if config_path.is_absolute():
            candidate_paths = [config_path]
        else:
            candidate_paths = [Path.cwd() / config_path, cls.PROJECT_ROOT_DIR / config_path]

        for candidate_path in candidate_paths:
            if candidate_path.is_file():
                return candidate_path

        raise FileNotFoundError(f"Configuration file not found. Searched in: {[str(p) for p in candidate_paths]}")

    @classmethod
    def load(cls, config_file: str | Path, default_configuration: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Load a YAML configuration file, merging its values over the default configuration
        :param config_file: Path of the YAML file (see resolve_path)
        :param default_configuration: Default values used for the parameters not defined in the file
        :return: The configuration dictionary
        """

        configuration: dict[str, Any] = dict(default_configuration or {})

        config_path = cls.resolve_path(config_file)
        with open(config_path, "r", encoding="utf-8") as file:
            file_configuration = yaml.safe_load(file) or {}

        # Merge the file values over the defaults (one level of nested sections, e.g., "rest" or "web")
        for key, value in file_configuration.items():
            if isinstance(value, dict) and isinstance(configuration.get(key), dict):
                configuration[key] = {**configuration[key], **value}
            else:
                configuration[key] = value

        print(f"Read Configuration from file ({config_path}): {configuration}")
        return configuration
