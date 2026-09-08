"""
MapGen Engine — Base Grid Generator (Abstract)

Defines the abstract interface that all procedural grid generators must
implement.  Uses the Template Method pattern: subclasses override
`generate()` while inheriting common seed/dimension management.

OOP Principles:
    - Abstraction:  ABC forces subclasses to implement `generate()`.
    - Encapsulation: Seed and dimensions are managed internally.
    - Open/Closed:  New algorithms extend this base without modifying it.
"""

from abc import ABC, abstractmethod


class BaseGridGenerator(ABC):
    """Abstract base class for all procedural 2-D grid generators.

    Attributes:
        _seed (int):   The RNG seed for reproducible generation.
        _width (int):  Horizontal cell count of the output grid.
        _height (int): Vertical cell count of the output grid.
    """

    def __init__(self, seed: int, width: int = 20, height: int = 20) -> None:
        """Initialise the generator with seed and grid dimensions.

        Args:
            seed:   Integer seed fed to the random number generator.
            width:  Number of columns in the grid (default 20).
            height: Number of rows in the grid (default 20).

        Raises:
            ValueError: If width or height is less than 1.
        """
        if width < 1 or height < 1:
            raise ValueError("Grid dimensions must be at least 1×1.")
        self._seed: int = seed
        self._width: int = width
        self._height: int = height

    # ── Abstract contract ────────────────────────────────────────────
    @abstractmethod
    def generate(self) -> list[list[int]]:
        """Generate and return a 2-D grid (list of rows).

        Each cell value is an integer:
            0 → Floor / open space
            1 → Wall / solid block

        Returns:
            A list of *height* rows, each containing *width* integers.
        """
        ...

    # ── Public accessors ─────────────────────────────────────────────
    def get_seed(self) -> int:
        """Return the RNG seed used by this generator."""
        return self._seed

    def get_dimensions(self) -> tuple[int, int]:
        """Return ``(width, height)`` of the grid."""
        return self._width, self._height

    # ── Dunder helpers ───────────────────────────────────────────────
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"seed={self._seed}, "
            f"width={self._width}, "
            f"height={self._height})"
        )
