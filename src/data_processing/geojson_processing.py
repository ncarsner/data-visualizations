import json


def read_geojson(file_path):
    """
    Reads a GeoJSON file and returns the data as a dictionary.

    :param file_path: Path to the GeoJSON file
    :return: GeoJSON data as a dictionary
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def get_feature_properties(geojson_data):
    """
    Extracts properties from all features in the GeoJSON data.

    :param geojson_data: GeoJSON data as a dictionary
    :return: List of properties dictionaries
    """
    properties = [feature["properties"] for feature in geojson_data["features"]]
    return properties


def filter_features_by_property(geojson_data, property_name, property_value):
    """
    Filters features in the GeoJSON data by a specific property value.

    :param geojson_data: GeoJSON data as a dictionary
    :param property_name: Name of the property to filter by
    :param property_value: Value of the property to filter by
    :return: Filtered GeoJSON data as a dictionary
    """
    filtered_features = [
        feature
        for feature in geojson_data["features"]
        if feature["properties"].get(property_name) == property_value
    ]
    return {"type": "FeatureCollection", "features": filtered_features}


def save_geojson(geojson_data, file_path):
    """
    Saves GeoJSON data to a file.

    :param geojson_data: GeoJSON data as a dictionary
    :param file_path: Path to the output GeoJSON file
    """
    with open(file_path, "w") as file:
        json.dump(geojson_data, file, indent=4)
