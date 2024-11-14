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


def main():
    input_file_path = "data/raw/geojson/Nashville_Building_Permit_applications.geojson"
    output_file_path = "data/processed/geojson/Nashville_Building_Permit_applications.geojson"
    # property_name = ''
    # property_value = ''
    res = read_geojson(input_file_path)
    save_geojson(res, output_file_path=output_file_path)

    properties = get_feature_properties(res)
    properties = get_unique_property_headers(res)
    properties = get_distinct_count_per_property(res)
    # print(json.dumps(properties, indent=4))

    # res_ppty = filter_features_by_property(res, 'Permit_Type_Description', 'Building Residential - Rehab')
    # print(res_ppty)


if __name__ == "__main__":
    main()
