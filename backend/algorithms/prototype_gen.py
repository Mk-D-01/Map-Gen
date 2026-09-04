"""
MapGen Engine — Prototype Grid Generator (Cellular Automata)

Concrete implementation of ``BaseGridGenerator`` that produces cave-like
2-D maps using a randomised fill followed by cellular-automata smoothing
passes.

Algorithm (simplified):
    1. Seed Python's ``random`` module for reproducibility.
    2. Fill a *width × height* matrix where each cell has a configurable
       probability of being a wall (default 45 %).
    3. Apply *N* smoothing passes (default 1):
       - If a cell's 8-neighbour wall count > 4 → becomes wall.
       - Otherwise → becomes floor.

OOP Principles:
    - Inheritance:    Extends ``BaseGridGenerator``.
    - Encapsulation:  Internal helpers are private (``_`` prefix).
    - SRP:            Each method has a single, clear responsibility.
"""

from __future__ import annotations

import random
from backend.algorithms.base import BaseGridGenerator


class PrototypeGridGenerator(BaseGridGenerator):
    """Cellular-automata cave generator.

    Attributes:
        _wall_probability (float): Chance each cell starts as a wall.
        _smooth_passes (int):      Number of smoothing iterations to apply.
    """

    def __init__(
        self,
        seed: int,
        width: int = 20,
        height: int = 20,
        wall_probability: float = 0.45,
        smooth_passes: int = 1,
    ) -> None:
        """Create a prototype generator.

        Args:
            seed:             RNG seed for reproducibility.
            width:            Grid column count.
            height:           Grid row count.
            wall_probability: Probability [0.0–1.0] each cell is initially a wall.
            smooth_passes:    Number of cellular-automata smoothing iterations.
        """
        super().__init__(seed, width, height)
        self._wall_probability: float = wall_probability
        self._smooth_passes: int = smooth_passes

    # ── Public API ───────────────────────────────────────────────────
    def generate(self) -> list[list[int]]:
        """Generate a smoothed cave map and return the 2-D grid.

        Returns:
            A list of *height* rows, each containing *width* ints (0 or 1).
        """
        random.seed(self._seed)
        grid = self._random_fill()
        for _ in range(self._smooth_passes):
            grid = self._smooth(grid)
        return grid

    # ── Private helpers ──────────────────────────────────────────────
    def _random_fill(self) -> list[list[int]]:
        """Create the initial random grid.

        Each cell is set to 1 (wall) with probability ``_wall_probability``,
        otherwise 0 (floor).

        Returns:
            Raw (un-smoothed) 2-D grid.
        """
        grid: list[list[int]] = []
        for _row in range(self._height):
            row: list[int] = []
            for _col in range(self._width):
                cell = 1 if random.random() < self._wall_probability else 0
                row.append(cell)
            grid.append(row)
        return grid

    def _smooth(self, grid: list[list[int]]) -> list[list[int]]:
        """Apply one cellular-automata smoothing pass.

        Rule: if a cell's Moore-neighbourhood wall count > 4, the cell
        becomes a wall; otherwise it becomes a floor.

        Args:
            grid: The grid to smooth.

        Returns:
            A new grid after one smoothing iteration.
        """
        new_grid: list[list[int]] = []
        for y in range(self._height):
            new_row: list[int] = []
            for x in range(self._width):
                wall_count = self._count_wall_neighbors(grid, x, y)
                new_row.append(1 if wall_count > 4 else 0)
            new_grid.append(new_row)
        return new_grid

    def _count_wall_neighbors(self, grid: list[list[int]], x: int, y: int) -> int:
        """Count the walls in the 8-cell Moore neighbourhood of *(x, y)*.

        Cells beyond the grid boundary are treated as walls (solid border).

        Args:
            grid: The current grid state.
            x:    Column index of the target cell.
            y:    Row index of the target cell.

        Returns:
            Integer count of neighbouring walls (0–8).
        """
        count = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue  # Skip the cell itself
                ny, nx = y + dy, x + dx
                # Out-of-bounds cells count as walls (solid border)
                if ny < 0 or ny >= self._height or nx < 0 or nx >= self._width:
                    count += 1
                elif grid[ny][nx] == 1:
                    count += 1
        return count

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"seed={self._seed}, "
            f"width={self._width}, "
            f"height={self._height}, "
            f"wall_prob={self._wall_probability}, "
            f"smooth_passes={self._smooth_passes})"
        )
