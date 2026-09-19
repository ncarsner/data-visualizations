import json

import geopandas as gpd
import pandas as pd
import pytest

from src.data_processing.cleaner import clean_data
from src.data_processing.export import export
from src.data_processing.geojson_processing import (
    get_distinct_count_per_property,
    get_feature_properties,
    get_unique_property_headers,
    read_geojson,
    save_geojson,
)
from src.data_processing.loader import load
from src.data_processing.transformer import filter_features_by_property, filter_shapefile


class TestGeoJsonProperties:
    def test_get_feature_properties_preserves_order(self, permits):
        properties = get_feature_properties(permits)
        assert [p["Const_Cost"] for p in properties] == [50000, 75000, 900000]

    def test_get_unique_property_headers(self, permits):
        assert get_unique_property_headers(permits) == {
            "Permit_Type_Description",
            "Date_Entered",
            "Const_Cost",
        }

    def test_get_unique_property_headers_unions_uneven_features(self):
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {"properties": {"a": 1}},
                {"properties": {"b": 2}},
            ],
        }
        assert get_unique_property_headers(geojson) == {"a", "b"}

    def test_get_distinct_count_per_property(self, permits):
        assert get_distinct_count_per_property(permits) == {
            "Permit_Type_Description": 2,
            "Date_Entered": 1,
            "Const_Cost": 3,
        }

    def test_distinct_count_returns_a_string_above_100_values(self):
        """
        Regression test for a type change callers cannot see coming.

        Above 100 distinct values the count is replaced by a sentence, so the
        returned dictionary mixes int and str values. This pins the current
        behavior; changing it is a breaking change for anything doing
        arithmetic on the result.
        """
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {"properties": {"many": i, "few": "constant"}} for i in range(101)
            ],
        }

        counts = get_distinct_count_per_property(geojson)

        assert counts["many"] == "Greater than 100 values"
        assert counts["few"] == 1

    def test_distinct_count_keeps_int_at_exactly_100_values(self):
        geojson = {
            "type": "FeatureCollection",
            "features": [{"properties": {"many": i}} for i in range(100)],
        }
        assert get_distinct_count_per_property(geojson) == {"many": 100}


class TestFiltering:
    def test_filter_features_by_property(self, permits):
        filtered = filter_features_by_property(
            permits, "Permit_Type_Description", "Building Residential - Rehab"
        )

        assert filtered["type"] == "FeatureCollection"
        assert len(filtered["features"]) == 2
        assert all(
            f["properties"]["Permit_Type_Description"] == "Building Residential - Rehab"
            for f in filtered["features"]
        )

    def test_filter_features_leaves_the_input_untouched(self, permits):
        filter_features_by_property(permits, "Permit_Type_Description", "no match")
        assert len(permits["features"]) == 3

    def test_filter_features_no_match_returns_empty_collection(self, permits):
        filtered = filter_features_by_property(permits, "Permit_Type_Description", "no match")
        assert filtered == {"type": "FeatureCollection", "features": []}

    def test_filter_features_missing_property_is_not_an_error(self, permits):
        filtered = filter_features_by_property(permits, "Nonexistent", "anything")
        assert filtered["features"] == []

    def test_filter_shapefile(self):
        gdf = gpd.GeoDataFrame(
            {"city": ["Nashville", "Memphis", "Nashville"], "n": [1, 2, 3]},
            geometry=gpd.points_from_xy([-86.8, -90.0, -86.7], [36.2, 35.1, 36.1]),
            crs="EPSG:4326",
        )

        filtered = filter_shapefile(gdf, "city", "Nashville")

        assert list(filtered["n"]) == [1, 3]
        assert isinstance(filtered, gpd.GeoDataFrame)


class TestCleaner:
    def test_clean_data_drops_nulls_and_duplicates(self):
        df = pd.DataFrame(
            {
                "district": [1, 1, 2, 3],
                "population": [100, 100, None, 300],
            }
        )

        cleaned = clean_data(df)

        assert len(cleaned) == 2
        assert list(cleaned["district"]) == [1, 3]

    def test_clean_data_leaves_the_input_untouched(self):
        df = pd.DataFrame({"a": [1, 1, None]})
        clean_data(df)
        assert len(df) == 3


class TestSaveGeoJson:
    def test_save_geojson_applies_the_limit(self, tmp_path, permits):
        destination = tmp_path / "permits.geojson"

        save_geojson(permits, destination, limit=2)

        written = json.loads(destination.read_text())
        assert len(written["features"]) == 2
        assert written["type"] == "FeatureCollection"

    def test_save_geojson_round_trips(self, tmp_path, permits):
        destination = tmp_path / "permits.geojson"
        save_geojson(permits, destination, limit=100)
        assert read_geojson(destination) == permits


class TestLoadExportDispatch:
    def test_csv_round_trip(self, tmp_path):
        destination = tmp_path / "districts.csv"
        df = pd.DataFrame({"DISTRICT": [5, 7], "POPULATION": [767871, 700000]})

        export(df, destination)

        pd.testing.assert_frame_equal(load(destination), df)

    def test_geojson_round_trip(self, tmp_path, permits):
        destination = tmp_path / "permits.geojson"
        export(permits, destination)
        assert load(destination) == permits

    def test_export_forwards_the_limit_keyword(self, tmp_path, permits):
        destination = tmp_path / "permits.geojson"
        export(permits, destination, limit=1)
        assert len(load(destination)["features"]) == 1

    def test_export_creates_missing_parent_directories(self, tmp_path, permits):
        destination = tmp_path / "does" / "not" / "exist" / "permits.geojson"

        written = export(permits, destination)

        assert written.exists()

    def test_export_returns_the_path(self, tmp_path, permits):
        destination = tmp_path / "permits.geojson"
        assert export(permits, destination) == destination

    @pytest.mark.parametrize("extension", [".parquet", ".txt", ""])
    def test_load_rejects_unsupported_extensions(self, tmp_path, extension):
        with pytest.raises(ValueError, match="No reader"):
            load(tmp_path / f"data{extension}")

    @pytest.mark.parametrize("extension", [".parquet", ".txt", ""])
    def test_export_rejects_unsupported_extensions(self, tmp_path, extension):
        with pytest.raises(ValueError, match="No writer"):
            export({}, tmp_path / f"data{extension}")

    def test_dispatch_ignores_extension_case(self, tmp_path, permits):
        destination = tmp_path / "permits.GEOJSON"
        export(permits, destination)
        assert load(destination) == permits


class TestCommittedData:
    """The pipeline's default inputs must stay loadable."""

    def test_raw_permits_load(self, repo_root):
        permits = load(
            repo_root / "data/raw/geojson/Nashville_Building_Permit_Applications.geojson"
        )
        assert permits["type"] == "FeatureCollection"
        assert permits["features"]

    def test_raw_districts_csv_loads(self, repo_root):
        districts = load(repo_root / "data/raw/csv/TN_Congressional_Districts.csv")
        assert {"DISTRICT", "NAME", "POPULATION"} <= set(districts.columns)
