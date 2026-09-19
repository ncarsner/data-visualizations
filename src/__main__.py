"""
Run the data processing and visualization pipeline.

    python -m src

Run from the repository root. Stages run in order:

    load -> clean -> transform -> export -> visualize -> save

Paths and parameters come from the environment, falling back to a .env file.
Copy .env.example to .env before the first run.
"""

from .data_processing.cleaner import clean_data
from .data_processing.export import export
from .data_processing.loader import load
from .data_processing.transformer import filter_features_by_property
from .utils.config import DEFAULT_ENV_FILE, ConfigurationError, load_config
from .utils.logging import get_logger, setup_logging
from .visualizations.folium_maps import build_map
from .visualizations.save_plots import save_map


def main(env_file=DEFAULT_ENV_FILE):
    setup_logging()
    logger = get_logger(__name__)
    config = load_config(env_file)

    # Load
    permits = load(config.raw_permits)
    districts_table = load(config.raw_districts_csv)
    logger.info("Loaded %d permit features and %d district rows",
                len(permits["features"]), len(districts_table))

    # Clean
    districts_table = clean_data(districts_table)

    # Transform
    permit_filter = config.permit_filter
    if permit_filter:
        filter_property, filter_value = permit_filter
        permits = filter_features_by_property(permits, filter_property, filter_value)
        logger.info("Filtered permits to %s == %r: %d features",
                    filter_property, filter_value, len(permits["features"]))

    # Export
    export(permits, config.processed_permits, limit=config.permit_limit)
    export(districts_table, config.processed_districts_csv)
    logger.info("Exported processed data to %s and %s",
                config.processed_permits, config.processed_districts_csv)

    # Visualize; the map reads the exported permits so it reflects PERMIT_LIMIT
    folium_map = build_map(
        districts=config.raw_districts,
        clinics=config.raw_clinics,
        permits=config.processed_permits,
    )

    # Save
    map_path = save_map(folium_map, config.reports_map)
    logger.info("Saved map to %s", map_path)


if __name__ == "__main__":
    try:
        main()
    except ConfigurationError as error:
        # A missing .env is the expected first-run state, not a crash.
        raise SystemExit(f"Configuration error: {error}")
