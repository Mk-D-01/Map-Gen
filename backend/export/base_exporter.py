"""
MapGen Engine — Base Exporter (Abstract)

Defines the abstract interface for all export formats.  Concrete
subclasses (PNG, JSON, SVG, etc.) implement ``export()`` to serialise
a 2-D grid matrix into a specific output format.

OOP Principles:
    - Abstraction:   ABC contract forces consistent export interface.
    - Open/Closed:   New formats extend this base without modifying it.
"""

from __future__ import annotations

import io
from abc import ABC, abstractmethod


class BaseExporter(ABC):
    """Abstract base class for grid-to-file exporters.

    Subclasses must implement both ``export`` (file path) and
    ``export_to_bytes`` (in-memory buffer) to support CLI and API usage.
    """

    @abstractmethod
    def export(self, matrix: list[list[int]], filename: str) -> str:
        """Export the *matrix* to a file on disk.

        Args:
            matrix:   2-D grid (list of rows of ints).
            filename: Destination file path.

        Returns:
            The absolute path of the saved file.
        """
        ...

    @abstractmethod
    def export_to_bytes(self, matrix: list[list[int]]) -> io.BytesIO:
        """Export the *matrix* to an in-memory byte buffer.

        Useful for streaming responses from the Flask API without
        touching the filesystem.

        Args:
            matrix: 2-D grid (list of rows of ints).

        Returns:
            A ``BytesIO`` buffer positioned at the start.
        """
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
