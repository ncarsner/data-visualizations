import folium
import random

# 20 most populous cities in the US with their latitude and longitude coordinates
cities = {
    "New York, NY": [40.7128, -74.0060],
    "Los Angeles, CA": [34.0522, -118.2437],
    "Chicago, IL": [41.8781, -87.6298],
    "Houston, TX": [29.7604, -95.3698],
    "Phoenix, AZ": [33.4484, -112.0740],
    "Philadelphia, PA": [39.9526, -75.1652],
    "San Antonio, TX": [29.4241, -98.4936],
    "San Diego, CA": [32.7157, -117.1611],
    "Dallas, TX": [32.7767, -96.7970],
    "San Jose, CA": [37.3382, -121.8863],
    "Austin, TX": [30.2672, -97.7431],
    "Jacksonville, FL": [30.3322, -81.6557],
    "Fort Worth, TX": [32.7555, -97.3308],
    "Columbus, OH": [39.9612, -82.9988],
    "Charlotte, NC": [35.2271, -80.8431],
    "San Francisco, CA": [37.7749, -122.4194],
    "Indianapolis, IN": [39.7684, -86.1581],
    "Seattle, WA": [47.6062, -122.3321],
    "Denver, CO": [39.7392, -104.9903],
    "Washington, DC": [38.9072, -77.0369],
    "Nashville, TN": [36.174465, -86.767960],
    "Portland, OR": [45.5051, -122.6750],
}

"""
This script generates an interactive map using the Folium library, centered on a randomly selected city from a predefined list of the 20 most populous cities in the US. The map includes a marker for the selected city and multiple tile layers that can be switched using a layer control.
Modules:
    folium: Used to create the map and add markers and tile layers.
    random: Used to randomly select a city from the list.
Data:
    cities (dict): A dictionary containing the names of the 20 most populous cities in the US as keys and their latitude and longitude coordinates as values.
Functions:
    None
Execution:
    - Selects a random city from the `cities` dictionary.
    - Creates a Folium map centered at the selected city's coordinates.
    - Adds a marker to the map for the selected city.
    - Adds multiple tile layers to the map.
    - Adds a layer control to switch between tile layers.
    - Saves the map to an HTML file named 'example_map.html'.
Icon Options:
    The `folium.Icon` class allows for various icon options, including:
    - 'cloud'
    - 'info-sign'
    - 'home'
    - 'ok-sign'
    - 'remove-sign'
    - 'star'
    - 'flag'
    - 'plus-sign'
    - 'minus-sign'
    - 'asterisk'
    - 'exclamation-sign'
    - 'gift'
    - 'leaf'
    - 'fire'
    - 'plane'
    - 'envelope'
    - 'pencil'
    - 'thumbs-up'
    - 'thumbs-down'
    - 'music'
    - 'heart'
"""

tn_congressional_districts = 'data/raw/geojson/tn_congressional_districts.geojson'
nash_bldg_permits = 'data/raw/geojson/Nashville_Building_Permit_Applications.geojson'

if __name__ == "__main__":
    # Select a random city from the dictionary
    city, coordinates = random.choice(list(cities.items()))

    city = "Nashville, TN"
    coordinates = [36.174465, -86.767960]

    # Initialize the map with no default tiles
    m = folium.Map(location=coordinates, zoom_start=14, tiles=None)

    # Add additional tile layers to the map
    # folium.TileLayer(
    #     "stamentoner",
    #     name="Stamen Toner",
    #     attr="Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.",
    # ).add_to(m)
    # folium.TileLayer(
    #     "stamenterrain",
    #     name="Stamen Terrain",
    #     attr="Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.",
    # ).add_to(m)
    folium.TileLayer(
        "cartodbdark_matter",
        name="CartoDB Dark Matter",
        attr="&copy; OpenStreetMap contributors & CartoDB",
    ).add_to(m)
    folium.TileLayer(
        "cartodbpositron",
        name="CartoDB Positron",
        attr="&copy; OpenStreetMap contributors & CartoDB",
    ).add_to(m)

    # Manually add OpenStreetMap as the first tile layer
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap").add_to(m)

    # Add Tennessee Congressional Districts GeoJSON data to the map
    folium.GeoJson(tn_congressional_districts, name="TN Congressional Districts", show=False).add_to(m)  # noqa: E501

    # Add Nashville Building Permit Applications GeoJSON data to the map
    folium.GeoJson(nash_bldg_permits, name="Nashville Building Permit Applications", show=False).add_to(m)  # noqa: E501

    # Add a marker to the map for the selected city
    folium.Marker(
        location=coordinates, popup=city, icon=folium.Icon(icon="home", color="orange")
    ).add_to(m)

    # # Set the default layer to OpenStreetMap tiles
    # folium.TileLayer("OpenStreetMap")

    # Add layer control to switch between tile layers
    folium.LayerControl().add_to(m)

    # Save the map to an HTML file
    m.save("example_map.html")
