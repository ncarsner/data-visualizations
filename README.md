# Data Visualization Project

## Project Overview

This project is designed to generate a series of data visualizations for analyzing and presenting insights from datasets. The primary objectives are to process raw data, transform it into a usable format, and produce various types of visualizations to highlight key patterns, trends, and correlations.

## Project Objectives

- **Data Collection and Processing**: Load and preprocess data from various sources.
- **Data Transformation**: Clean and transform data into formats suitable for visualization.
- **Visualization Generation**: Create a range of static and interactive visualizations, including bar charts, line plots, and heatmaps.
- **Report Generation**: Save visualizations and summary reports to facilitate insights and analysis.

## Directory Structure

This project follows a structured directory setup to separate various components, enhancing modularity, readability, and maintainability.

```plaintext
data_visualization_project/
├── data/
│   ├── raw/            # Raw datasets, usually in CSV, JSON, or other formats
│   ├── processed/      # Processed data ready for visualization (e.g. cleaned or aggregated data)
│   └── external/       # External data files or reference datasets
│
├── src/
│   ├── __init__.py          # Initialization for the src package
│   ├── config.ini           # Configuration settings for the project (paths, parameters)
│   ├── data_processing/
│   │   ├── __init__.py      # Initialization for the data processing module
│   │   ├── loader.py        # Script to load data (from files, APIs, databases)
│   │   ├── cleaner.py       # Script to clean and preprocess raw data
│   │   ├── transformer.py   # Script for transforming data (e.g. aggregating or filtering)
│   │   └── export.py        # Export processed data for visualization
│   │
│   ├── visualizations/
│   │   ├── __init__.py      # Initialization for the visualizations module
│   │   ├── bar_charts.py    # Module for creating bar chart visualizations
│   │   ├── line_plots.py    # Module for creating line plot visualizations
│   │   ├── heatmaps.py      # Module for creating heatmaps
│   │   └── save_plots.py    # Module to handle saving/exporting plots in desired formats
│   │
│   ├── utils/
│   │   ├── __init__.py      # Initialization for the utils module
│   │   ├── logging.py       # Logging utilities for tracking processes
│   │   ├── helpers.py       # Helper functions used across modules
│   │   └── plot_styles.py   # Custom styles or themes for visualizations
│   │
│   └── __main__.py          # Main script to run the project (e.g. workflow orchestration)
│
├── reports/
│   ├── figures/             # Directory for saving generated figures
│   └── summary/             # Summarized reports or insights generated
│
├── tests/
│   ├── __init__.py                 # Initialization for the tests package
│   ├── test_data_processing.py     # Tests for data processing module
│   ├── test_visualizations.py      # Tests for visualization functions
│   └── test_utils.py               # Tests for utility functions
│
├── notebooks/
│   ├── exploratory_analysis.ipynb  # Jupyter Notebook for exploratory data analysis
│   └── testing_visuals.ipynb       # Notebook for testing visualization styles and plots
│
├── .gitignore          # Git ignore file
├── requirements.txt    # Python dependencies for the project
└── README.md           # Project description and setup instructions
```

## Directory Details

#### `data/`
- **`raw/`**: Contains raw datasets in various formats <i>(e.g., CSV, JSON)</i> as originally collected.
- **`processed/`**: Stores processed data, ready for visualization. Data here is typically cleaned and transformed.
- **`external/`**: Holds any external data or reference files used in analysis.

#### `src/`
- `config.ini`: Where configuration settings such as file paths and parameters, should be set.
- **`data_processing/`**: Responsible for data loading, cleaning, and transformation. Each module focuses on a specific aspect of data processing.
  - `loader.py`: Handles data loading from various sources <i>(e.g., files, APIs)</i>.
  - `cleaner.py`: Performs data cleaning, handling missing values, and data inconsistencies.
  - `transformer.py`: Conducts data transformations, such as aggregations and filtering.
  - `export.py`: Exports processed data for visualization.
- **`visualizations/`**: Contains modules for different types of visualizations.
  - `bar_charts.py`, `line_plots.py`, `heatmaps.py`: Specific modules for creating distinct types of visualizations.
  - `save_plots.py`: Manages exporting and saving visualizations.
- **utils/**: Utility scripts with general-purpose functions.
  - `logging.py`: Provides logging functions for debugging and tracking project activity.
  - `helpers.py`: Contains commonly used helper functions.
  - `plot_styles.py`: Defines custom plot styles or themes.
- **main.py**: Orchestrates the workflow, running data processing and visualization generation in sequence.

### `reports/`
- **`figures/`**: Stores generated visualizations.
- **`summary/`**: Contains summary reports, such as markdown or text files with key insights.

### `tests/`
- Contains unit tests to verify the accuracy of data processing and visualization modules.
  - `test_data_processing.py`: Tests for data loading, cleaning, and transformation.
  - `test_visualizations.py`: Tests for visualization functions.
  - `test_utils.py`: Tests for utility functions.

### `notebooks/`
- **exploratory_analysis.ipynb**: Jupyter notebook for exploratory data analysis (EDA) to understand the dataset.
- **testing_visuals.ipynb**: Notebook to test and preview visualization styles.

## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd data_visualization_project
   ```

2. **Install Dependencies**:
   Use the provided `requirements.txt` to install necessary packages.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Project**:
   Execute the main script to run the complete workflow.
   ```bash
   python src/main.py
   ```

## License

This project is licensed under the MIT License.
