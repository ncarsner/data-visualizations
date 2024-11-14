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

    Parameters:
    geojson (dict): The GeoJSON object.
    from_crs (str): The source CRS in EPSG code format.
    to_crs (str): The target CRS in EPSG code format.

    Returns:
    dict: Transformed GeoJSON object.
    """
    project = pyproj.Transformer.from_crs(from_crs, to_crs, always_xy=True).transform

    def transform_coords(coords):
        if isinstance(coords[0], (list, tuple)):
            return [transform_coords(c) for c in coords]
        else:
            point = Point(*coords)
            transformed_point = transform(project, point)
            return transformed_point.x, transformed_point.y

    geojson["coordinates"] = transform_coords(geojson["coordinates"])
    return geojson
