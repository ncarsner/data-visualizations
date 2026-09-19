"""End-to-end tests for `python -m src`, run against the committed datasets."""

import json

import pandas as pd
import pytest

from src.__main__ import main


@pytest.fixture
def pipeline(tmp_path, repo_root, monkeypatch):
    """
    Run the pipeline from the repository root, writing outputs to tmp_path.

    Inputs are the committed raw datasets; every output path is redirected so
    a test run cannot overwrite tracked files.
    """

    def run(permit_limit=5, filter_property="", filter_value=""):
        config = tmp_path / "paths.ini"
        config.write_text(
            f"""
[raw]
permits = data/raw/geojson/Nashville_Building_Permit_Applications.geojson
clinics = data/raw/geojson/Public_Health_Clinics.geojson
districts = data/raw/geojson/TN_Congressional_Districts.geojson
districts_csv = data/raw/csv/TN_Congressional_Districts.csv

[processed]
permits = {tmp_path / "permits.geojson"}
districts_csv = {tmp_path / "districts.csv"}

[reports]
map = {tmp_path / "figures" / "map.html"}

[parameters]
permit_limit = {permit_limit}
permit_filter_property = {filter_property}
permit_filter_value = {filter_value}
"""
        )
        monkeypatch.chdir(repo_root)
        main(str(config))
        return {
            "permits": tmp_path / "permits.geojson",
            "districts": tmp_path / "districts.csv",
            "map": tmp_path / "figures" / "map.html",
        }

    return run


def test_pipeline_writes_every_output(pipeline):
    outputs = pipeline()

    assert outputs["permits"].exists()
    assert outputs["districts"].exists()
    assert outputs["map"].exists()


def test_permit_limit_is_applied(pipeline):
    outputs = pipeline(permit_limit=5)

    written = json.loads(outputs["permits"].read_text())
    assert len(written["features"]) == 5


def test_filter_is_applied_before_the_limit(pipeline):
    outputs = pipeline(
        permit_limit=10,
        filter_property="Permit_Type_Description",
        filter_value="Building Residential - Rehab",
    )

    written = json.loads(outputs["permits"].read_text())
    assert len(written["features"]) == 10
    assert all(
        feature["properties"]["Permit_Type_Description"]
        == "Building Residential - Rehab"
        for feature in written["features"]
    )


def test_districts_are_cleaned(pipeline):
    outputs = pipeline()

    districts = pd.read_csv(outputs["districts"])
    assert not districts.isnull().values.any()
    assert not districts.duplicated().any()


def test_the_map_draws_the_exported_permits(pipeline):
    """The map reads the processed file, so permit_limit reaches the map."""
    outputs = pipeline(permit_limit=3)

    html = outputs["map"].read_text()
    assert "Nashville Building Permits" in html
    assert "Congressional Districts" in html


def test_output_directories_are_created(pipeline):
    outputs = pipeline()
    assert outputs["map"].parent.is_dir()
