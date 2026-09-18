from pathlib import Path

from .csv_processing import load_csv
from .geojson_processing import read_geojson
from .shapefile_processing import read_shapefile

_READERS = {
    ".csv": load_csv,
    ".geojson": read_geojson,
    ".shp": read_shapefile,
}


def load(file_path):
    """
    Load a dataset, selecting the reader from the file extension.

    Parameters:
    file_path (str or Path): Path to a .csv, .geojson, or .shp file.

    Returns:
    pd.DataFrame for .csv, dict (FeatureCollection) for .geojson,
    or GeoDataFrame for .shp.

    Raises:
    ValueError: If the file extension has no registered reader.
    """
    suffix = Path(file_path).suffix.lower()
    if suffix not in _READERS:
        raise ValueError(
            f"No reader for '{suffix}' files. Supported: {', '.join(sorted(_READERS))}"
        )
    return _READERS[suffix](file_path)
