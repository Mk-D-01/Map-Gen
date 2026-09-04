"""
MapGen Engine — Flask Application (OOP)

Uses an ``MapGenApp`` factory class that encapsulates Flask app creation,
CORS configuration, and route registration.  The generator class and
exporter instance are injected as dependencies, keeping the app open
for extension with new algorithms and export formats.

Routes:
    GET  /health       → {"status": "ok"}
    POST /api/generate → accepts {seed, width, height}, returns {matrix, seed}
    POST /api/export   → accepts {seed, width, height}, returns PNG download

OOP Principles:
    - Encapsulation:          Flask app and config wrapped in a class.
    - Dependency Injection:   Generator class and exporter are pluggable.
    - Single Responsibility:  Routing logic separated from generation logic.
"""

from __future__ import annotations

import sys
import os

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

# Ensure the project root is importable when run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.algorithms.base import BaseGridGenerator
from backend.algorithms.prototype_gen import PrototypeGridGenerator
from backend.export.base_exporter import BaseExporter
from backend.export.prototype_export import PNGExporter


class MapGenApp:
    """Factory class that builds and configures the Flask application.

    Attributes:
        _app (Flask):                       The wrapped Flask instance.
        _generator_class (type):            The grid generator class to use.
        _exporter (BaseExporter):           The exporter instance for PNG output.
    """

    def __init__(
        self,
        generator_class: type[BaseGridGenerator] = PrototypeGridGenerator,
        exporter: BaseExporter | None = None,
    ) -> None:
        """Create the MapGen application.

        Args:
            generator_class: A *class* (not instance) that subclasses
                             ``BaseGridGenerator``.  Instantiated per request.
            exporter:        An exporter instance.  Defaults to ``PNGExporter()``.
        """
        self._generator_class = generator_class
        self._exporter = exporter or PNGExporter()
        self._app = Flask(__name__)
        CORS(self._app)  # Allow cross-origin requests from the frontend
        self._register_routes()

    # ── Public API ───────────────────────────────────────────────────
    def create_app(self) -> Flask:
        """Return the configured Flask app (for WSGI servers / testing)."""
        return self._app

    # ── Route registration ───────────────────────────────────────────
    def _register_routes(self) -> None:
        """Wire up all REST API routes on the Flask app."""

        @self._app.route("/health", methods=["GET"])
        def health_check():
            """Liveness probe – returns 200 with status ok."""
            return jsonify({"status": "ok"}), 200

        @self._app.route("/api/generate", methods=["POST"])
        def generate_map():
            """Generate a 2-D grid from a seed and return as JSON.

            Expects JSON body:
                {
                    "seed":   int   (required),
                    "width":  int   (optional, default 20),
                    "height": int   (optional, default 20)
                }

            Returns JSON:
                {
                    "matrix": [[int, ...], ...],
                    "seed":   int
                }
            """
            data = request.get_json(force=True)

            seed = data.get("seed", 42)
            width = data.get("width", 20)
            height = data.get("height", 20)

            # Validate inputs
            try:
                seed = int(seed)
                width = int(width)
                height = int(height)
            except (TypeError, ValueError):
                return jsonify({"error": "seed, width, and height must be integers"}), 400

            if width < 1 or height < 1:
                return jsonify({"error": "width and height must be at least 1"}), 400

            # Generate via the injected generator class
            generator = self._generator_class(seed=seed, width=width, height=height)
            matrix = generator.generate()

            return jsonify({"matrix": matrix, "seed": seed}), 200

        @self._app.route("/api/export", methods=["POST"])
        def export_map():
            """Generate a grid and return it as a downloadable PNG.

            Expects the same JSON body as ``/api/generate``.
            Returns a ``image/png`` binary response.
            """
            data = request.get_json(force=True)

            seed = data.get("seed", 42)
            width = data.get("width", 20)
            height = data.get("height", 20)

            try:
                seed = int(seed)
                width = int(width)
                height = int(height)
            except (TypeError, ValueError):
                return jsonify({"error": "seed, width, and height must be integers"}), 400

            if width < 1 or height < 1:
                return jsonify({"error": "width and height must be at least 1"}), 400

            generator = self._generator_class(seed=seed, width=width, height=height)
            matrix = generator.generate()

            png_buffer = self._exporter.export_to_bytes(matrix)

            return send_file(
                png_buffer,
                mimetype="image/png",
                as_attachment=True,
                download_name=f"mapgen_seed{seed}_{width}x{height}.png",
            )

    def __repr__(self) -> str:
        return (
            f"MapGenApp(generator={self._generator_class.__name__}, "
            f"exporter={self._exporter!r})"
        )


# ── Entry point ──────────────────────────────────────────────────────
# Run directly:  python -m backend.app
#   or:          python backend/app.py

if __name__ == "__main__":
    app_wrapper = MapGenApp()
    flask_app = app_wrapper.create_app()
    print(f"  🗺️  MapGen Engine API running on http://localhost:5000")
    print(f"  {app_wrapper!r}")
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
