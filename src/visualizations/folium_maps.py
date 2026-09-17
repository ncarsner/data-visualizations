"""
Interactive Folium maps of Nashville and Tennessee geospatial datasets.

build_map() layers congressional districts, public health clinics, and building
permit applications over switchable base tiles, and returns the map. Persist it
with save_plots.save_map().

Icon options:
    folium.Icon accepts Bootstrap glyphicon names, including:
    'cloud', 'info-sign', 'home', 'ok-sign', 'remove-sign', 'star', 'flag',
    'plus-sign', 'minus-sign', 'asterisk', 'exclamation-sign', 'gift', 'leaf',
    'fire', 'plane', 'envelope', 'pencil', 'thumbs-up', 'thumbs-down', 'music',
    'heart'
"""

import folium

# Most populous US cities, plus Nashville, as [latitude, longitude]
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


def build_map(districts, clinics, permits, location=None, zoom_start=14):
    """
    Build a layered map of districts, clinics, and building permits.

    Each dataset may be a GeoJSON file path or an in-memory FeatureCollection.
    Data layers start hidden and are toggled from the layer control.

    Parameters:
    districts (str or dict): Congressional districts; popups show DISTRICT.
    clinics (str or dict): Public health clinics; popups show ClinicName, Address, Hours.
    permits (str or dict): Building permit applications; popups show
        Permit_Type_Description, Date_Entered, Const_Cost.
    location (list): [latitude, longitude] map center. Default is Nashville, TN.
    zoom_start (int): Initial zoom level. Default is 14.

    Returns:
    folium.Map: The assembled map.
    """
    if location is None:
        location = cities["Nashville, TN"]

    m = folium.Map(location=location, zoom_start=zoom_start, tiles=None)

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
    folium.TileLayer(
        "openstreetmap",
        name="OpenStreetMap",
        attr="&copy; OpenStreetMap contributors",
    ).add_to(m)

    folium.GeoJson(
        data=districts,
        name="Congressional Districts",
        show=False,
        popup=folium.GeoJsonPopup(fields=["DISTRICT"], labels=True),
        marker=folium.Marker(icon=folium.Icon(icon="flag", color="red")),
    ).add_to(m)

    folium.GeoJson(
        data=clinics,
        name="Public Health Clinics",
        show=False,
        popup=folium.GeoJsonPopup(fields=["ClinicName", "Address", "Hours"], labels=True),
        marker=folium.Marker(icon=folium.Icon(icon="plus-sign", color="blue")),
    ).add_to(m)

    folium.GeoJson(
        data=permits,
        name="Nashville Building Permits",
        show=False,
        popup=folium.GeoJsonPopup(
            fields=["Permit_Type_Description", "Date_Entered", "Const_Cost"], labels=True
        ),
        marker=folium.Marker(icon=folium.Icon(icon="home", color="orange")),
    ).add_to(m)

    folium.LayerControl().add_to(m)
    return m
