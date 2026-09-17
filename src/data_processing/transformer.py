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


def filter_shapefile(gdf, column_name, value):
    """
    Filters a GeoDataFrame based on a column value.

    Parameters:
    gdf (GeoDataFrame): The GeoDataFrame to filter.
    column_name (str): The column name to filter on.
    value: The value to filter by.

    Returns:
    GeoDataFrame: The filtered GeoDataFrame.
    """
    return gdf[gdf[column_name] == value]
