from pathlib import Path

from .csv_processing import save_cleaned_data
from .geojson_processing import save_geojson
from .shapefile_processing import save_shapefile

_WRITERS = {
    ".csv": save_cleaned_data,
    ".geojson": save_geojson,
    ".shp": save_shapefile,
}


def export(data, file_path, **kwargs):
    """
    Write a dataset, selecting the writer from the file extension.

    Parent directories are created if they do not exist.

    Parameters:
    data: pd.DataFrame for .csv, dict (FeatureCollection) for .geojson,
        or GeoDataFrame for .shp.
    file_path (str or Path): Destination path.
    **kwargs: Passed to the underlying writer, e.g. ``limit`` for GeoJSON.

    Returns:
    Path: The path written.

    Raises:
    ValueError: If the file extension has no registered writer.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix not in _WRITERS:
        raise ValueError(
            f"No writer for '{suffix}' files. Supported: {', '.join(sorted(_WRITERS))}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    _WRITERS[suffix](data, path, **kwargs)
    return path
