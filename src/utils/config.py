"""
Project configuration, read from environment variables.

Values come from the process environment, falling back to a ``.env`` file in
the repository root. Real environment variables win, so a shell export or a CI
secret overrides the file without editing it.

``.env`` is not version-controlled. Copy ``.env.example`` to ``.env`` to get a
working set of defaults.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_ENV_FILE = ".env"

# Every path the pipeline reads or writes. All are required; there are no
# built-in defaults, so a misconfigured run fails immediately and by name
# rather than reading or writing somewhere unexpected.
REQUIRED_PATHS = {
    "raw_permits": "RAW_PERMITS",
    "raw_clinics": "RAW_CLINICS",
    "raw_districts": "RAW_DISTRICTS",
    "raw_districts_csv": "RAW_DISTRICTS_CSV",
    "processed_permits": "PROCESSED_PERMITS",
    "processed_districts_csv": "PROCESSED_DISTRICTS_CSV",
    "reports_map": "REPORTS_MAP",
}


class ConfigurationError(RuntimeError):
    """Raised when the environment does not describe a runnable pipeline."""


@dataclass(frozen=True)
class Config:
    """Resolved pipeline configuration."""

    raw_permits: Path
    raw_clinics: Path
    raw_districts: Path
    raw_districts_csv: Path
    processed_permits: Path
    processed_districts_csv: Path
    reports_map: Path
    permit_limit: int = 100
    permit_filter_property: str = ""
    permit_filter_value: str = ""

    @property
    def permit_filter(self):
        """
        The property and value to filter permits by, or None for no filtering.

        Both halves are required; setting only one is treated as unset, so a
        half-filled .env cannot silently drop every feature.
        """
        if self.permit_filter_property and self.permit_filter_value:
            return self.permit_filter_property, self.permit_filter_value
        return None


def load_config(env_file=DEFAULT_ENV_FILE):
    """
    Read configuration from the environment, loading ``env_file`` first.

    Parameters:
    env_file (str or Path): Path to a .env file. Missing files are ignored,
        which is what a deployment setting real environment variables wants.

    Returns:
    Config: The resolved configuration.

    Raises:
    ConfigurationError: If a required path is unset, or if PERMIT_LIMIT is
        not a positive integer.
    """
    load_dotenv(env_file)

    missing = [name for name in REQUIRED_PATHS.values() if not os.environ.get(name)]
    if missing:
        raise ConfigurationError(
            f"Missing required configuration: {', '.join(missing)}. "
            f"Copy .env.example to {os.fspath(env_file)} and edit it, "
            "or set these as environment variables."
        )

    paths = {
        field: Path(os.environ[name]) for field, name in REQUIRED_PATHS.items()
    }

    return Config(
        **paths,
        permit_limit=_positive_int("PERMIT_LIMIT", default=100),
        permit_filter_property=os.environ.get("PERMIT_FILTER_PROPERTY", "").strip(),
        permit_filter_value=os.environ.get("PERMIT_FILTER_VALUE", "").strip(),
    )


def _positive_int(name, default):
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        raise ConfigurationError(f"{name} must be an integer, got {raw!r}") from None
    if value < 1:
        raise ConfigurationError(f"{name} must be at least 1, got {value}")
    return value
