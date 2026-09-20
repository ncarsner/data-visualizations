from pathlib import Path

import matplotlib

# Tests must not open windows; select a non-interactive backend before any
# module imports pyplot.
matplotlib.use("Agg")

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

# Everything load_config reads. Cleared before each test so the suite cannot
# pick up a developer's exported variables, and so values that python-dotenv
# writes into os.environ do not leak from one test into the next.
CONFIG_VARIABLES = (
    "RAW_PERMITS",
    "RAW_CLINICS",
    "RAW_DISTRICTS",
    "RAW_DISTRICTS_CSV",
    "PROCESSED_PERMITS",
    "PROCESSED_DISTRICTS_CSV",
    "REPORTS_MAP",
    "PERMIT_LIMIT",
    "PERMIT_FILTER_PROPERTY",
    "PERMIT_FILTER_VALUE",
)


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Run every test against an environment that configures nothing."""
    for name in CONFIG_VARIABLES:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture(scope="session")
def repo_root():
    """The repository root, so tests do not depend on the working directory."""
    return REPO_ROOT


@pytest.fixture
def permits():
    """A small permits FeatureCollection shaped like the real dataset."""
    return {
        "type": "FeatureCollection",
        "features": [
            _permit("Building Residential - Rehab", 50000, [-86.78, 36.17]),
            _permit("Building Residential - Rehab", 75000, [-86.77, 36.16]),
            _permit("Building Commercial - New", 900000, [-86.79, 36.18]),
        ],
    }


@pytest.fixture
def clinics():
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-86.78, 36.17]},
                "properties": {
                    "ClinicName": "Lentz Public Health Center",
                    "Address": "2500 Charlotte Ave",
                    "Hours": "M-F 7:30-4:00",
                },
            }
        ],
    }


@pytest.fixture
def districts():
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-86.9, 36.0],
                            [-86.6, 36.0],
                            [-86.6, 36.3],
                            [-86.9, 36.3],
                            [-86.9, 36.0],
                        ]
                    ],
                },
                "properties": {"DISTRICT": 5, "NAME": "Fifth", "POPULATION": 767871},
            }
        ],
    }


def _permit(permit_type, cost, coordinates):
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": coordinates},
        "properties": {
            "Permit_Type_Description": permit_type,
            "Date_Entered": "2024-01-15",
            "Const_Cost": cost,
        },
    }
