# Data Visualization Project

## Project Overview

A small pipeline for processing and mapping public geospatial datasets for Nashville and Tennessee. It reads raw GeoJSON, CSV and shapefile data, filters and cleans it, writes processed copies, and renders an interactive Folium map of congressional districts, public health clinics and building permit applications.

The package is organized in three layers:

| Layer | Package | Responsibility |
|---|---|---|
| Data processing | `src/data_processing/` | Load, clean, transform and export data |
| Visualization | `src/visualizations/` | Build figures and maps, and save them |
| Utilities | `src/utils/` | Configuration, logging, geospatial and file helpers |

`src/__main__.py` runs them in sequence.

## Data

Every dataset in `data/raw/` is geospatial and covers Nashville or Tennessee. The same three subjects are provided both as GeoJSON and as Esri shapefiles.

| Dataset | Features | Geometry | Notable properties |
|---|---|---|---|
| Nashville building permit applications | 5,812 | Point | `Permit__`, `Permit_Type_Description`, `Date_Issued`, `Const_Cost`, `Address` |
| Public health clinics | 4 | Point | `ClinicName`, `Phone`, `Hours`, `Address` |
| TN congressional districts | 9 | Polygon | `DISTRICT`, `NAME`, `POPULATION` |

`data/raw/csv/TN_Congressional_Districts.csv` holds the district attribute table without geometry: `OBJECTID`, `DISTRICT`, `NAME`, `POPULATION`.

Permits are the only large dataset, so the pipeline caps how many features it exports and draws (`permit_limit`, default 100). Processed output lands in `data/processed/`, which is not version-controlled; `data/raw/` is, so a fresh clone can run the pipeline without downloading anything.

## Running the pipeline

From the repository root:

```bash
python -m src
```

Stages run in order, reading every path and parameter from `config/paths.ini`:

| Stage | Module | What it does |
|---|---|---|
| Load | `data_processing.loader` | Reads the raw permits GeoJSON and the districts CSV |
| Clean | `data_processing.cleaner` | Drops null and duplicate rows from the districts table |
| Transform | `data_processing.transformer` | Filters permits by one property; skipped unless configured |
| Export | `data_processing.export` | Writes processed permits and the cleaned districts CSV |
| Visualize | `visualizations.folium_maps` | Builds the layered map |
| Save | `visualizations.save_plots` | Writes the map to `reports/figures/` |

Outputs:

| Path | Content |
|---|---|
| `data/processed/geojson/Nashville_Building_Permit_Applications.geojson` | First `permit_limit` permit features after filtering |
| `data/processed/csv/TN_Congressional_Districts.csv` | Cleaned districts table |
| `reports/figures/nashville_map.html` | Interactive map |

The map opens on Nashville with three switchable base layers (CartoDB Dark Matter, CartoDB Positron, OpenStreetMap) and three data layers that start hidden and are toggled from the layer control. Clicking a feature opens a popup: the district number, a clinic's name, address and hours, or a permit's type, entry date and construction cost.

## Configuration

Configuration lives in `config/`, not in the package. Paths are relative to the repository root.

### `config/paths.ini`

| Section | Key | Purpose |
|---|---|---|
| `[raw]` | `permits`, `clinics`, `districts`, `districts_csv` | Input files |
| `[processed]` | `permits`, `districts_csv` | Processed data outputs |
| `[reports]` | `map` | Map output |
| `[parameters]` | `permit_limit` | Maximum permit features exported and drawn. Default `100` |
| `[parameters]` | `permit_filter_property`, `permit_filter_value` | Keep only permits whose property equals this value. Both empty (the default) disables filtering |

To run against a different configuration file:

```python
from src.__main__ import main
main("path/to/other.ini")
```

### `config/logging.ini`

Read by `utils.logging.setup_logging()`. Defines a console handler and a file handler writing to `sample.log`.

## Directory Structure

```plaintext
data-visualizations/
├── config/
│   ├── logging.ini          # Logging configuration
│   └── paths.ini            # Input/output paths and pipeline parameters
│
├── data/
│   ├── raw/
│   │   ├── csv/             # District attribute table
│   │   ├── geojson/         # Permits, clinics, districts
│   │   └── shapefiles/      # The same three subjects as Esri shapefiles
│   └── processed/
│       └── geojson/         # Pipeline output
│
├── src/
│   ├── __init__.py
│   ├── __main__.py               # Pipeline entry point (python -m src)
│   │
│   ├── data_processing/
│   │   ├── __init__.py
│   │   ├── loader.py             # load(path) — reader chosen by file extension
│   │   ├── cleaner.py            # Drop nulls and duplicates
│   │   ├── transformer.py        # Filter GeoJSON features and GeoDataFrames
│   │   ├── export.py             # export(data, path) — writer chosen by extension
│   │   ├── csv_processing.py     # CSV reader/writer
│   │   ├── geojson_processing.py # GeoJSON reader/writer and property inspection
│   │   └── shapefile_processing.py  # Shapefile reader/writer
│   │
│   ├── visualizations/
│   │   ├── __init__.py
│   │   ├── folium_maps.py        # Layered interactive maps
│   │   ├── matplotlib_plots.py   # Histogram, scatter, line, boxplot
│   │   ├── plotly_interactive.py # Plotly examples
│   │   └── save_plots.py         # Save figures, plotly figures and maps
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py             # Read config/paths.ini
│       ├── logging.py            # Configure logging from config/logging.ini
│       ├── geo_utils.py          # CRS transforms
│       ├── file_utils.py         # Text file helpers
│       └── plot_styles.py        # Seaborn plot styling
│
├── reports/
│   ├── figures/             # Generated figures and maps
│   └── summary/             # Summary reports
│
├── examples/
│   └── startup_ages.py      # Standalone matplotlib example, synthetic data
│
├── notebooks/               # Exploratory Jupyter notebooks
├── tests/                   # pytest suite
│
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

Visualization modules are named after their rendering backend rather than the chart type, because the map work has no meaningful home under a chart-type layout.

## Using the modules directly

`loader.load` and `export.export` dispatch on the file extension, so callers do not need to know which format module to reach for.

```python
from src.data_processing.export import export
from src.data_processing.loader import load
from src.data_processing.transformer import filter_features_by_property

permits = load("data/raw/geojson/Nashville_Building_Permit_Applications.geojson")
rehabs = filter_features_by_property(permits, "Permit_Type_Description", "Building Residential - Rehab")
export(rehabs, "data/processed/geojson/rehabs.geojson", limit=50)
```

| Extension | `load` returns | `export` accepts |
|---|---|---|
| `.csv` | `pandas.DataFrame` | `pandas.DataFrame` |
| `.geojson` | `dict` (FeatureCollection) | `dict`; `limit` caps features written |
| `.shp` | `geopandas.GeoDataFrame` | `geopandas.GeoDataFrame` |

Any other extension raises `ValueError`. `export` creates parent directories as needed.

Plot functions return their figure and display it by default. Pass `show=False` to save without opening a window:

```python
from src.visualizations.matplotlib_plots import plot_histogram
from src.visualizations.save_plots import save_figure

fig = plot_histogram(values, title="Construction cost", show=False)
save_figure(fig, "reports/figures/cost.png")
```

`save_plots` also provides `save_plotly_figure` (HTML) and `save_map` (Folium). Each creates parent directories and returns the written path.

## Getting Started

1. **Clone the repository**

   ```bash
   git clone <repository_url>
   cd data-visualizations
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   `geopandas`, `pyproj` and `shapely` are built on the GDAL, PROJ and GEOS C libraries. Current releases ship prebuilt wheels for common platforms, so `pip install` usually needs no system packages; if a build is attempted from source, install those libraries first (`brew install gdal proj geos`, or `apt-get install gdal-bin libgdal-dev proj-bin libgeos-dev`).

   `requirements.txt` lists dependencies without version constraints, so a fresh install resolves to current releases.

3. **Run the pipeline**

   ```bash
   python -m src
   ```

## Notebooks and examples

`notebooks/us_population.ipynb` plots synthetic US population data and is unrelated to the geospatial pipeline. `examples/startup_ages.py` is a standalone matplotlib chart of synthetic funding-round data, kept as a plotting reference. Neither is part of the pipeline.

## Tests

```bash
pytest
```

The suite uses only the committed raw datasets and pytest's `tmp_path`, so it never writes into the working tree.

| Module | Covers |
|---|---|
| `test_data_processing.py` | GeoJSON property inspection, filtering, cleaning, and `load`/`export` dispatch including unsupported extensions |
| `test_utils.py` | CRS transforms against the Web Mercator closed form, file helpers, configuration loading |
| `test_visualizations.py` | Plot functions returning figures, the three `save_plots` writers, map layers and popups |
| `test_pipeline.py` | `main()` end to end: outputs written, `permit_limit` applied, filtering applied before the limit |
| `test_imports.py` | Every module imports, and importing one writes no files |

## Planned

Known gaps, none of them addressed yet. They are listed here so the sections above can be read as a description of what the repository actually does.

- **`get_distinct_count_per_property` changes return type.** Above 100 distinct values it returns the string `"Greater than 100 values"` in place of an `int`, so the dictionary it returns mixes types. A regression test pins the current behavior; fixing it is a breaking change.
- **Plotly.** `visualizations/plotly_interactive.py` contains demonstration functions that load Plotly's sample datasets and display them. They do not return figures, so they cannot be passed to `save_plotly_figure`.
- **Logging verbosity.** `config/logging.ini` sets the root logger to `DEBUG`. Third-party libraries imported after `setup_logging()` emit large volumes of debug output.
- **Basemap tiles.** Folium warns that CartoDB basemap tiles now require an API key. The Dark Matter and Positron layers may not render without one; the OpenStreetMap layer is unaffected.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
