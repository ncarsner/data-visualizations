"""
Import smoke test.

Every module in the package must import cleanly. Before this suite existed,
`src.visualizations` raised ImportError on a symbol that never existed and
`shapefile_processing` raised on a placeholder path at import time; neither
was caught until someone tried to run the project.
"""

import importlib
import pkgutil

import pytest

import src

MODULES = sorted(
    module.name
    for module in pkgutil.walk_packages(src.__path__, prefix="src.")
    # __main__ runs the pipeline; it is covered by test_pipeline.py instead.
    if module.name != "src.__main__"
)


def test_the_walk_found_the_packages():
    """Guard against the parametrized test passing because nothing was found."""
    assert {"src.data_processing", "src.utils", "src.visualizations"} <= set(MODULES)


@pytest.mark.parametrize("module_name", MODULES)
def test_module_imports(module_name):
    importlib.import_module(module_name)


def test_importing_a_module_writes_no_files(tmp_path, monkeypatch):
    """Import must not execute example code against the filesystem."""
    monkeypatch.chdir(tmp_path)

    for module_name in MODULES:
        importlib.reload(importlib.import_module(module_name))

    assert list(tmp_path.iterdir()) == []
