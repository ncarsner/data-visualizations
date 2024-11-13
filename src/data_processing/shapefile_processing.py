import geopandas as gpd


def read_shapefile(file_path):
    """
    Reads a shapefile and returns a GeoDataFrame.

    Parameters:
    file_path (str): The path to the shapefile.

    Returns:
    GeoDataFrame: The GeoDataFrame containing the shapefile data.
    """
    return gpd.read_file(file_path)


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


def save_shapefile(gdf, output_path):
    """
    Saves a GeoDataFrame to a shapefile.

    Parameters:
    gdf (GeoDataFrame): The GeoDataFrame to save.
    output_path (str): The path to save the shapefile.
    """
    gdf.to_file(output_path)


# Example usage:
gdf = read_shapefile('path/to/shapefile.shp')
filtered_gdf = filter_shapefile(gdf, 'column_name', 'value')
save_shapefile(filtered_gdf, 'path/to/output.shp')
