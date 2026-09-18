"""
Run the data processing and visualization pipeline.

    python -m src

Run from the repository root. Stages run in order:

    load -> clean -> transform -> export -> visualize -> save

Paths and parameters are read from config/paths.ini.
"""

from .data_processing.cleaner import clean_data
from .data_processing.export import export
from .data_processing.loader import load
from .data_processing.transformer import filter_features_by_property
from .utils.config import load_config
from .utils.logging import get_logger, setup_logging
from .visualizations.folium_maps import build_map
from .visualizations.save_plots import save_map


def main(config_path="config/paths.ini"):
    setup_logging()
    logger = get_logger(__name__)
    config = load_config(config_path)
    raw, processed, reports = config["raw"], config["processed"], config["reports"]
    parameters = config["parameters"]

    # Load
    permits = load(raw["permits"])
    districts_table = load(raw["districts_csv"])
    logger.info("Loaded %d permit features and %d district rows",
                len(permits["features"]), len(districts_table))

    # Clean
    districts_table = clean_data(districts_table)

    # Transform
    filter_property = parameters.get("permit_filter_property")
    filter_value = parameters.get("permit_filter_value")
    if filter_property and filter_value:
        permits = filter_features_by_property(permits, filter_property, filter_value)
        logger.info("Filtered permits to %s == %r: %d features",
                    filter_property, filter_value, len(permits["features"]))

    # Export
    permit_limit = parameters.getint("permit_limit")
    export(permits, processed["permits"], limit=permit_limit)
    export(districts_table, processed["districts_csv"])
    logger.info("Exported processed data to %s and %s",
                processed["permits"], processed["districts_csv"])

    # Visualize; the map reads the exported permits so it reflects permit_limit
    folium_map = build_map(
        districts=raw["districts"],
        clinics=raw["clinics"],
        permits=processed["permits"],
    )

    # Save
    map_path = save_map(folium_map, reports["map"])
    logger.info("Saved map to %s", map_path)


if __name__ == "__main__":
    main()
