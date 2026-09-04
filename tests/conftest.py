"""
MapGen Engine — Pytest Fixtures

Provides reusable fixtures for the test suite:
    - ``generator``:   A ``PrototypeGridGenerator`` instance seeded with 42.
    - ``flask_client``: A Flask test client for API endpoint testing.
    - ``exporter``:    A ``PNGExporter`` instance with default settings.
"""

from __future__ import annotations

import sys
import os

import pytest

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.algorithms.prototype_gen import PrototypeGridGenerator
from backend.export.prototype_export import PNGExporter
from backend.app import MapGenApp


@pytest.fixture
def generator() -> PrototypeGridGenerator:
    """Return a default prototype generator with seed 42."""
    return PrototypeGridGenerator(seed=42, width=20, height=20)


@pytest.fixture
def exporter() -> PNGExporter:
    """Return a default PNG exporter."""
    return PNGExporter()


@pytest.fixture
def flask_client():
    """Return a Flask test client for the MapGen API."""
    app_wrapper = MapGenApp()
    flask_app = app_wrapper.create_app()
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client
