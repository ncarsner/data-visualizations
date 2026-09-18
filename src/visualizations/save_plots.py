from pathlib import Path


def _prepare(file_path):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_figure(fig, file_path, dpi=150):
    """
    Save a matplotlib figure.

    Parameters:
    fig (matplotlib.figure.Figure): The figure to save.
    file_path (str or Path): Destination; the format follows the extension (.png, .svg, .pdf).
    dpi (int): Resolution for raster formats. Default is 150.

    Returns:
    Path: The path written.
    """
    path = _prepare(file_path)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


def save_plotly_figure(fig, file_path):
    """
    Save a Plotly figure as interactive HTML.

    Parameters:
    fig (plotly.graph_objects.Figure): The figure to save.
    file_path (str or Path): Destination .html path.

    Returns:
    Path: The path written.
    """
    path = _prepare(file_path)
    fig.write_html(path)
    return path


def save_map(folium_map, file_path):
    """
    Save a Folium map as a standalone HTML page.

    Parameters:
    folium_map (folium.Map): The map to save.
    file_path (str or Path): Destination .html path.

    Returns:
    Path: The path written.
    """
    path = _prepare(file_path)
    folium_map.save(str(path))
    return path
