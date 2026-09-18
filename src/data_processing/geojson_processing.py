import json


def read_geojson(input_file_path, encoding="utf-8"):
    """
    Reads a GeoJSON file and returns the data as a dictionary.

    :param input_file_path: Path to the input GeoJSON file
    :param encoding: Encoding of the GeoJSON file
    :return: GeoJSON data as a dictionary
    """
    with open(input_file_path, "r", encoding=encoding) as file:
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


def get_unique_property_headers(geojson_data):
    """
    Extracts unique property headers from all features in the GeoJSON data.

    :param geojson_data: GeoJSON data as a dictionary
    :return: Set of unique property headers
    """
    unique_headers = set()
    for feature in geojson_data["features"]:
        unique_headers.update(feature["properties"].keys())
    return unique_headers

def get_distinct_count_per_property(geojson_data):
    """
    Returns the distinct count of values for each property header in the GeoJSON data.

    :param geojson_data: GeoJSON data as a dictionary
    :return: Dictionary with property headers as keys and distinct count of values as values
    """
    distinct_counts = {}
    for feature in geojson_data["features"]:
        for key, value in feature["properties"].items():
            if key not in distinct_counts:
                distinct_counts[key] = set()
            distinct_counts[key].add(value)
    
    for key in distinct_counts:
        if len(distinct_counts[key]) > 100:
            distinct_counts[key] = "Greater than 100 values"
        else:
            distinct_counts[key] = len(distinct_counts[key])
    
    return distinct_counts

def save_geojson(geojson_data, output_file_path, limit=100):
    """
    Saves GeoJSON data to a file with an option to limit the number of records.

    :param geojson_data: GeoJSON data as a dictionary
    :param output_file_path: Path to the output GeoJSON file
    :param limit: Maximum number of records to include in the output file
    """
    limited_features = geojson_data["features"][:limit]
    limited_geojson_data = {"type": "FeatureCollection", "features": limited_features}
    
    with open(output_file_path, "w") as file:
        json.dump(limited_geojson_data, file, indent=4)
