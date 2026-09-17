from shapely.geometry import Point, mapping, shape
from shapely.ops import transform
import pyproj


def transform_coordinates(x, y, from_crs="EPSG:4326", to_crs="EPSG:3857"):
    """
    Transform coordinates from one CRS to another.

    Parameters:
    x (float): The x coordinate (longitude).
    y (float): The y coordinate (latitude).
    from_crs (str): The source CRS in EPSG code format.
    to_crs (str): The target CRS in EPSG code format.

    Returns:
    tuple: Transformed coordinates (x, y).
    """
    project = pyproj.Transformer.from_crs(from_crs, to_crs, always_xy=True).transform
    point = Point(x, y)
    transformed_point = transform(project, point)
    return transformed_point.x, transformed_point.y


def transform_geojson(geojson, from_crs="EPSG:4326", to_crs="EPSG:3857"):
    """
    Transform GeoJSON coordinates from one CRS to another.

    Accepts a bare geometry, a Feature, or a FeatureCollection. The input is
    left unmodified; a transformed copy is returned.

    Parameters:
    geojson (dict): A geometry, Feature, or FeatureCollection.
    from_crs (str): The source CRS in EPSG code format.
    to_crs (str): The target CRS in EPSG code format.

    Returns:
    dict: Transformed GeoJSON object of the same type as the input.
    """
    project = pyproj.Transformer.from_crs(from_crs, to_crs, always_xy=True).transform

    def transform_geometry(geometry):
        if geometry is None:
            return None
        return mapping(transform(project, shape(geometry)))

    geojson_type = geojson.get("type")

    if geojson_type == "FeatureCollection":
        return {
            **geojson,
            "features": [
                {**feature, "geometry": transform_geometry(feature.get("geometry"))}
                for feature in geojson["features"]
            ],
        }

    if geojson_type == "Feature":
        return {**geojson, "geometry": transform_geometry(geojson.get("geometry"))}

    return transform_geometry(geojson)
