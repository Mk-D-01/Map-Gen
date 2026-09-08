"""
MapGen Engine — PNG Exporter (Pillow)

Concrete implementation of ``BaseExporter`` that renders a 2-D grid
matrix into a PNG image using the Pillow library.

Each cell is drawn as a square of ``cell_size`` × ``cell_size`` pixels.
Wall cells (1) default to black and floor cells (0) default to white.

OOP Principles:
    - Inheritance:    Extends ``BaseExporter``.
    - Encapsulation:  Rendering configuration is private.
    - SRP:            Only responsible for PNG serialisation.
"""

from __future__ import annotations

import io
import os
from PIL import Image, ImageDraw

from backend.export.base_exporter import BaseExporter


class PNGExporter(BaseExporter):
    """Exports a 2-D integer grid to a PNG image.

    Attributes:
        _cell_size (int):     Pixel width/height of each grid cell.
        _wall_color (tuple):  RGB colour for wall cells (value 1).
        _floor_color (tuple): RGB colour for floor cells (value 0).
    """

    def __init__(
        self,
        cell_size: int = 20,
        wall_color: tuple[int, int, int] = (0, 0, 0),
        floor_color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        """Initialise the PNG exporter.

        Args:
            cell_size:   Pixel size per grid cell (default 20).
            wall_color:  RGB tuple for walls (default black).
            floor_color: RGB tuple for floors (default white).
        """
        self._cell_size: int = cell_size
        self._wall_color: tuple[int, int, int] = wall_color
        self._floor_color: tuple[int, int, int] = floor_color

    # ── Public API ───────────────────────────────────────────────────
    def export(self, matrix: list[list[int]], filename: str = "output_prototype.png") -> str:
        """Render *matrix* to a PNG file on disk.

        Args:
            matrix:   2-D grid of integers (0 = floor, 1 = wall).
            filename: Output file path (default ``output_prototype.png``).

        Returns:
            Absolute path of the saved PNG file.
        """
        image = self._render_image(matrix)
        abs_path = os.path.abspath(filename)
        image.save(abs_path, format="PNG")
        return abs_path

    def export_to_bytes(self, matrix: list[list[int]]) -> io.BytesIO:
        """Render *matrix* to an in-memory PNG byte buffer.

        Args:
            matrix: 2-D grid of integers.

        Returns:
            A ``BytesIO`` buffer containing the PNG data, seeked to 0.
        """
        image = self._render_image(matrix)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    # ── Private helpers ──────────────────────────────────────────────
    def _render_image(self, matrix: list[list[int]]) -> Image.Image:
        """Create a Pillow ``Image`` from the grid matrix.

        Args:
            matrix: 2-D grid of integers.

        Returns:
            A Pillow ``Image`` object ready to be saved or streamed.
        """
        height = len(matrix)
        width = len(matrix[0]) if height > 0 else 0

        img_width = width * self._cell_size
        img_height = height * self._cell_size

        image = Image.new("RGB", (img_width, img_height), self._floor_color)
        draw = ImageDraw.Draw(image)

        for y, row in enumerate(matrix):
            for x, cell in enumerate(row):
                color = self._wall_color if cell == 1 else self._floor_color
                x0 = x * self._cell_size
                y0 = y * self._cell_size
                x1 = x0 + self._cell_size
                y1 = y0 + self._cell_size
                draw.rectangle([x0, y0, x1, y1], fill=color)

        return image

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"cell_size={self._cell_size}, "
            f"wall={self._wall_color}, "
            f"floor={self._floor_color})"
        )
