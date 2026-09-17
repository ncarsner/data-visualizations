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


def save_shapefile(gdf, output_path):
    """
    Saves a GeoDataFrame to a shapefile.

    Parameters:
    gdf (GeoDataFrame): The GeoDataFrame to save.
    output_path (str): The path to save the shapefile.
    """
    gdf.to_file(output_path)


# Example usage:
# gdf = read_shapefile("data/raw/shapefiles/Public_Health_Clinics.shp")
# filtered_gdf = transformer.filter_shapefile(gdf, "column_name", "value")
# save_shapefile(filtered_gdf, "data/processed/shapefiles/Public_Health_Clinics.shp")
