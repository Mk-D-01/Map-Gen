"""
MapGen Engine — Prototype Test Suite

Tests covering:
    1. Seed reproducibility (deterministic generation).
    2. Grid dimension correctness.
    3. Cell value validity (only 0 and 1).
    4. Flask /health endpoint (HTTP 200).
    5. Flask /api/generate endpoint (returns valid matrix JSON).
    6. Flask /api/export endpoint (returns PNG bytes).
    7. PNG exporter produces valid image bytes.
"""

from __future__ import annotations

import json
import io

from backend.algorithms.prototype_gen import PrototypeGridGenerator


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ALGORITHM TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestSeedReproducibility:
    """Verify that the same seed always produces the same grid."""

    def test_seed_reproducibility(self):
        """Running generate_prototype_grid(42) twice yields identical grids."""
        gen1 = PrototypeGridGenerator(seed=42)
        gen2 = PrototypeGridGenerator(seed=42)

        grid1 = gen1.generate()
        grid2 = gen2.generate()

        assert grid1 == grid2, "Same seed must produce identical grids"

    def test_different_seeds_differ(self):
        """Different seeds should (almost certainly) produce different grids."""
        gen1 = PrototypeGridGenerator(seed=42)
        gen2 = PrototypeGridGenerator(seed=999)

        grid1 = gen1.generate()
        grid2 = gen2.generate()

        assert grid1 != grid2, "Different seeds should produce different grids"


class TestGridDimensions:
    """Verify output grid dimensions match the requested size."""

    def test_default_dimensions(self, generator):
        """Default 20×20 generator produces a 20-row × 20-col grid."""
        grid = generator.generate()

        assert len(grid) == 20, "Grid should have 20 rows"
        assert all(len(row) == 20 for row in grid), "Each row should have 20 columns"

    def test_custom_dimensions(self):
        """Custom width/height are respected."""
        gen = PrototypeGridGenerator(seed=7, width=10, height=15)
        grid = gen.generate()

        assert len(grid) == 15, "Grid should have 15 rows"
        assert all(len(row) == 10 for row in grid), "Each row should have 10 columns"


class TestCellValues:
    """Verify cells only contain valid values."""

    def test_cells_are_binary(self, generator):
        """Every cell in the grid must be 0 or 1."""
        grid = generator.generate()

        for row in grid:
            for cell in row:
                assert cell in (0, 1), f"Cell value {cell} is not 0 or 1"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FLASK API TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestHealthEndpoint:
    """Verify the /health liveness probe."""

    def test_health_check(self, flask_client):
        """GET /health returns HTTP 200 with status ok."""
        response = flask_client.get("/health")

        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"


class TestGenerateEndpoint:
    """Verify the /api/generate REST endpoint."""

    def test_generate_returns_matrix(self, flask_client):
        """POST /api/generate returns a valid matrix and seed."""
        response = flask_client.post(
            "/api/generate",
            data=json.dumps({"seed": 42, "width": 10, "height": 10}),
            content_type="application/json",
        )

        assert response.status_code == 200

        data = response.get_json()
        assert "matrix" in data
        assert "seed" in data
        assert data["seed"] == 42

        matrix = data["matrix"]
        assert len(matrix) == 10
        assert all(len(row) == 10 for row in matrix)

    def test_generate_bad_dimensions(self, flask_client):
        """POST /api/generate with invalid dimensions returns 400."""
        response = flask_client.post(
            "/api/generate",
            data=json.dumps({"seed": 1, "width": 0, "height": 5}),
            content_type="application/json",
        )

        assert response.status_code == 400


class TestExportEndpoint:
    """Verify the /api/export REST endpoint."""

    def test_export_returns_png(self, flask_client):
        """POST /api/export returns a PNG image (binary)."""
        response = flask_client.post(
            "/api/export",
            data=json.dumps({"seed": 42, "width": 5, "height": 5}),
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.content_type == "image/png"
        # PNG files start with an 8-byte signature
        assert response.data[:4] == b"\x89PNG"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  EXPORTER TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestPNGExporter:
    """Verify the PNG exporter produces valid image data."""

    def test_export_to_bytes(self, exporter, generator):
        """export_to_bytes returns a BytesIO with valid PNG data."""
        grid = generator.generate()
        buffer = exporter.export_to_bytes(grid)

        assert isinstance(buffer, io.BytesIO)
        data = buffer.read()
        assert len(data) > 0, "PNG buffer should not be empty"
        assert data[:4] == b"\x89PNG", "Buffer should contain PNG signature"
