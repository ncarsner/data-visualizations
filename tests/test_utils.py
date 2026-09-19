import math
from pathlib import Path

import pytest

from src.utils.config import REQUIRED_PATHS, ConfigurationError, load_config
from src.utils.file_utils import (
    append_to_file,
    delete_file,
    file_exists,
    read_file,
    write_file,
)
from src.utils.geo_utils import transform_coordinates, transform_geojson

# Web Mercator (EPSG:3857) is defined over a sphere of this radius.
EARTH_CIRCUMFERENCE_HALF = 20037508.342789244


def web_mercator(longitude, latitude):
    """EPSG:4326 -> EPSG:3857 from the closed form, independent of pyproj."""
    x = longitude * EARTH_CIRCUMFERENCE_HALF / 180
    y = math.log(math.tan((90 + latitude) * math.pi / 360)) / (math.pi / 180)
    return x, y * EARTH_CIRCUMFERENCE_HALF / 180


class TestTransformCoordinates:
    def test_origin_is_unchanged(self):
        assert transform_coordinates(0, 0) == pytest.approx((0, 0), abs=1e-6)

    def test_nashville_matches_the_closed_form(self):
        longitude, latitude = -86.767960, 36.174465

        assert transform_coordinates(longitude, latitude) == pytest.approx(
            web_mercator(longitude, latitude), rel=1e-9
        )

    def test_round_trip_returns_the_input(self):
        longitude, latitude = -86.767960, 36.174465

        x, y = transform_coordinates(longitude, latitude)
        back = transform_coordinates(x, y, from_crs="EPSG:3857", to_crs="EPSG:4326")

        assert back == pytest.approx((longitude, latitude), abs=1e-9)


class TestTransformGeoJson:
    def test_transforms_a_bare_geometry(self):
        geometry = {"type": "Point", "coordinates": [-86.767960, 36.174465]}

        transformed = transform_geojson(geometry)

        assert transformed["type"] == "Point"
        assert transformed["coordinates"] == pytest.approx(
            web_mercator(-86.767960, 36.174465), rel=1e-9
        )

    def test_transforms_a_feature_and_keeps_properties(self):
        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-86.767960, 36.174465]},
            "properties": {"ClinicName": "Lentz"},
        }

        transformed = transform_geojson(feature)

        assert transformed["properties"] == {"ClinicName": "Lentz"}
        assert transformed["geometry"]["coordinates"] == pytest.approx(
            web_mercator(-86.767960, 36.174465), rel=1e-9
        )

    def test_transforms_every_feature_in_a_collection(self, permits):
        transformed = transform_geojson(permits)

        assert transformed["type"] == "FeatureCollection"
        assert len(transformed["features"]) == 3
        for original, result in zip(permits["features"], transformed["features"]):
            assert result["geometry"]["coordinates"] == pytest.approx(
                web_mercator(*original["geometry"]["coordinates"]), rel=1e-9
            )
            assert result["properties"] == original["properties"]

    def test_leaves_the_input_unmodified(self, permits):
        before = permits["features"][0]["geometry"]["coordinates"][:]

        transform_geojson(permits)

        assert permits["features"][0]["geometry"]["coordinates"] == before

    def test_null_geometry_passes_through(self):
        feature_collection = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "geometry": None, "properties": {"a": 1}}
            ],
        }

        transformed = transform_geojson(feature_collection)

        assert transformed["features"][0]["geometry"] is None
        assert transformed["features"][0]["properties"] == {"a": 1}


class TestFileUtils:
    def test_write_then_read(self, tmp_path):
        path = tmp_path / "notes.txt"

        write_file(path, "first")

        assert read_file(path) == "first"

    def test_write_replaces_existing_content(self, tmp_path):
        path = tmp_path / "notes.txt"
        write_file(path, "first")

        write_file(path, "second")

        assert read_file(path) == "second"

    def test_append_adds_to_existing_content(self, tmp_path):
        path = tmp_path / "notes.txt"
        write_file(path, "first")

        append_to_file(path, " and second")

        assert read_file(path) == "first and second"

    def test_append_creates_a_missing_file(self, tmp_path):
        path = tmp_path / "notes.txt"

        append_to_file(path, "content")

        assert read_file(path) == "content"

    def test_file_exists(self, tmp_path):
        path = tmp_path / "notes.txt"
        assert not file_exists(path)

        write_file(path, "content")

        assert file_exists(path)

    def test_file_exists_is_false_for_a_directory(self, tmp_path):
        assert not file_exists(tmp_path)

    def test_delete_file(self, tmp_path):
        path = tmp_path / "notes.txt"
        write_file(path, "content")

        delete_file(path)

        assert not file_exists(path)

    def test_delete_missing_file_is_a_no_op(self, tmp_path):
        delete_file(tmp_path / "never_existed.txt")


ENV_EXAMPLE_PATHS = """
RAW_PERMITS=data/raw/geojson/Nashville_Building_Permit_Applications.geojson
RAW_CLINICS=data/raw/geojson/Public_Health_Clinics.geojson
RAW_DISTRICTS=data/raw/geojson/TN_Congressional_Districts.geojson
RAW_DISTRICTS_CSV=data/raw/csv/TN_Congressional_Districts.csv
PROCESSED_PERMITS=out/permits.geojson
PROCESSED_DISTRICTS_CSV=out/districts.csv
REPORTS_MAP=out/map.html
"""


@pytest.fixture
def env_file(tmp_path, clean_env):
    """Write a .env in tmp_path; returns a callable taking extra lines."""

    def write(extra=""):
        path = tmp_path / ".env"
        path.write_text(ENV_EXAMPLE_PATHS + extra)
        return path

    return write


class TestLoadConfig:
    def test_reads_every_path(self, env_file):
        config = load_config(env_file())

        assert config.raw_permits == Path(
            "data/raw/geojson/Nashville_Building_Permit_Applications.geojson"
        )
        assert config.raw_clinics == Path("data/raw/geojson/Public_Health_Clinics.geojson")
        assert config.raw_districts_csv == Path("data/raw/csv/TN_Congressional_Districts.csv")
        assert config.processed_permits == Path("out/permits.geojson")
        assert config.reports_map == Path("out/map.html")

    def test_paths_are_path_objects(self, env_file):
        config = load_config(env_file())

        assert all(
            isinstance(getattr(config, field), Path) for field in REQUIRED_PATHS
        )

    def test_permit_limit_defaults_to_100(self, env_file):
        assert load_config(env_file()).permit_limit == 100

    def test_permit_limit_is_read_from_the_file(self, env_file):
        assert load_config(env_file("PERMIT_LIMIT=25\n")).permit_limit == 25

    def test_blank_permit_limit_falls_back_to_the_default(self, env_file):
        assert load_config(env_file("PERMIT_LIMIT=\n")).permit_limit == 100

    @pytest.mark.parametrize("value", ["abc", "1.5", "ten"])
    def test_non_integer_permit_limit_raises(self, env_file, value):
        with pytest.raises(ConfigurationError, match="PERMIT_LIMIT must be an integer"):
            load_config(env_file(f"PERMIT_LIMIT={value}\n"))

    @pytest.mark.parametrize("value", ["0", "-5"])
    def test_permit_limit_below_one_raises(self, env_file, value):
        with pytest.raises(ConfigurationError, match="at least 1"):
            load_config(env_file(f"PERMIT_LIMIT={value}\n"))

    def test_missing_required_path_raises_naming_it(self, tmp_path, clean_env):
        path = tmp_path / ".env"
        path.write_text(
            ENV_EXAMPLE_PATHS.replace(
                "RAW_CLINICS=data/raw/geojson/Public_Health_Clinics.geojson", ""
            )
        )

        with pytest.raises(ConfigurationError, match="RAW_CLINICS"):
            load_config(path)

    def test_absent_env_file_raises_with_a_usable_message(self, tmp_path, clean_env):
        with pytest.raises(ConfigurationError, match="Copy .env.example"):
            load_config(tmp_path / "absent.env")

    def test_environment_variables_win_over_the_file(self, env_file, monkeypatch):
        monkeypatch.setenv("PERMIT_LIMIT", "7")
        monkeypatch.setenv("REPORTS_MAP", "elsewhere/map.html")

        config = load_config(env_file("PERMIT_LIMIT=25\n"))

        assert config.permit_limit == 7
        assert config.reports_map == Path("elsewhere/map.html")


class TestPermitFilter:
    def test_unset_means_no_filtering(self, env_file):
        assert load_config(env_file()).permit_filter is None

    def test_both_halves_set_returns_the_pair(self, env_file):
        config = load_config(
            env_file("PERMIT_FILTER_PROPERTY=Permit_Type_Description\nPERMIT_FILTER_VALUE=Rehab\n")
        )

        assert config.permit_filter == ("Permit_Type_Description", "Rehab")

    @pytest.mark.parametrize(
        "extra",
        [
            "PERMIT_FILTER_PROPERTY=Permit_Type_Description\n",
            "PERMIT_FILTER_VALUE=Rehab\n",
        ],
    )
    def test_half_a_filter_is_ignored(self, env_file, extra):
        """Filtering on a property with no value would drop every feature."""
        assert load_config(env_file(extra)).permit_filter is None

    def test_whitespace_is_stripped(self, env_file):
        config = load_config(
            env_file("PERMIT_FILTER_PROPERTY=  \nPERMIT_FILTER_VALUE=Rehab\n")
        )

        assert config.permit_filter is None


class TestCommittedEnvExample:
    """.env.example must stay usable, since the README tells readers to copy it."""

    def test_it_describes_a_runnable_pipeline(self, repo_root, clean_env, monkeypatch):
        monkeypatch.chdir(repo_root)

        config = load_config(repo_root / ".env.example")

        assert config.raw_permits.is_file()
        assert config.raw_clinics.is_file()
        assert config.raw_districts.is_file()
        assert config.raw_districts_csv.is_file()
        assert config.permit_limit > 0
        assert config.permit_filter is None

    def test_it_sets_every_required_variable(self, repo_root):
        text = (repo_root / ".env.example").read_text()

        for name in REQUIRED_PATHS.values():
            assert f"{name}=" in text
