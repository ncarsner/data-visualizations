import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pytest
from matplotlib.figure import Figure

from src.visualizations.folium_maps import build_map, cities
from src.visualizations.matplotlib_plots import (
    plot_boxplot,
    plot_histogram,
    plot_line,
    plot_scatter,
)
from src.visualizations.save_plots import save_figure, save_map, save_plotly_figure


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


class TestMatplotlibPlots:
    def test_plot_histogram_returns_a_figure(self):
        assert isinstance(plot_histogram([1, 2, 2, 3], show=False), Figure)

    def test_plot_scatter_returns_a_figure(self):
        assert isinstance(plot_scatter([1, 2, 3], [4, 5, 6], show=False), Figure)

    def test_plot_line_returns_a_figure(self):
        assert isinstance(plot_line([1, 2, 3], [4, 5, 6], show=False), Figure)

    def test_plot_boxplot_returns_a_figure(self):
        assert isinstance(plot_boxplot([1, 2, 3, 10], show=False), Figure)

    def test_show_false_does_not_display(self, monkeypatch):
        shown = []
        monkeypatch.setattr(plt, "show", lambda *args, **kwargs: shown.append(True))

        plot_histogram([1, 2, 3], show=False)

        assert shown == []

    def test_show_true_displays(self, monkeypatch):
        shown = []
        monkeypatch.setattr(plt, "show", lambda *args, **kwargs: shown.append(True))

        plot_histogram([1, 2, 3], show=True)

        assert shown == [True]

    def test_title_reaches_the_figure(self):
        fig = plot_histogram([1, 2, 3], title="Construction cost", show=False)
        assert fig.axes[0].get_title() == "Construction cost"


class TestSavePlots:
    def test_save_figure_writes_a_png(self, tmp_path):
        fig = plot_histogram([1, 2, 3], show=False)
        destination = tmp_path / "histogram.png"

        written = save_figure(fig, destination)

        assert written == destination
        assert destination.read_bytes().startswith(b"\x89PNG")

    def test_save_figure_honors_the_extension(self, tmp_path):
        fig = plot_histogram([1, 2, 3], show=False)
        destination = tmp_path / "histogram.svg"

        save_figure(fig, destination)

        assert "<svg" in destination.read_text()

    def test_save_figure_creates_missing_directories(self, tmp_path):
        fig = plot_histogram([1, 2, 3], show=False)
        destination = tmp_path / "figures" / "nested" / "histogram.png"

        save_figure(fig, destination)

        assert destination.exists()

    def test_save_plotly_figure_writes_html(self, tmp_path):
        fig = go.Figure(data=go.Scatter(x=[1, 2], y=[3, 4]))
        destination = tmp_path / "scatter.html"

        written = save_plotly_figure(fig, destination)

        assert written == destination
        assert "plotly" in destination.read_text().lower()

    def test_save_map_writes_html(self, tmp_path, districts, clinics, permits):
        folium_map = build_map(districts, clinics, permits)
        destination = tmp_path / "maps" / "nashville.html"

        written = save_map(folium_map, destination)

        assert written == destination
        assert "folium" in destination.read_text().lower()


class TestBuildMap:
    def test_defaults_to_nashville(self, districts, clinics, permits):
        folium_map = build_map(districts, clinics, permits)
        assert folium_map.location == cities["Nashville, TN"]

    def test_location_and_zoom_are_configurable(self, districts, clinics, permits):
        folium_map = build_map(
            districts, clinics, permits, location=cities["Austin, TX"], zoom_start=9
        )

        assert folium_map.location == cities["Austin, TX"]
        assert folium_map.options["zoom"] == 9

    def test_every_layer_is_present(self, districts, clinics, permits):
        html = build_map(districts, clinics, permits).get_root().render()

        for name in (
            "CartoDB Dark Matter",
            "CartoDB Positron",
            "OpenStreetMap",
            "Congressional Districts",
            "Public Health Clinics",
            "Nashville Building Permits",
        ):
            assert name in html

    def test_accepts_file_paths(self, tmp_path, repo_root, permits):
        """Datasets may be paths as well as in-memory collections."""
        raw = repo_root / "data" / "raw" / "geojson"

        folium_map = build_map(
            districts=str(raw / "TN_Congressional_Districts.geojson"),
            clinics=str(raw / "Public_Health_Clinics.geojson"),
            permits=permits,
        )

        assert save_map(folium_map, tmp_path / "map.html").exists()

    def test_popup_fields_render(self, districts, clinics, permits):
        html = build_map(districts, clinics, permits).get_root().render()

        assert "ClinicName" in html
        assert "Permit_Type_Description" in html
