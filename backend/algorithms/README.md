# 🧠 Backend Algorithms — Procedural Map Generators

Welcome to the **Algorithms** directory! This is the brain room where all procedural map generation magic happens.

---

## 🧒 Explain Like I'm 5 (ELI5)

> Imagine you want to draw a secret cave system on graph paper:
>
> 1. **Rulebook** (`BaseGridGenerator`): Every map painter must agree on how big the graph paper is (`width` and `height`) and what magic seed number to use.
> 2. **Cave Generator** (`PrototypeGridGenerator`):
>    - First, flip a coin for every square on the paper. Heads = fill in a wall (1), Tails = leave as open floor (0).
>    - Next, run a **smoothing pass**: look at each square's 8 neighbours. If 5 or more neighbours are walls, turn this square into a wall too!
>    - Shazam! The jagged random dots turn into smooth, beautiful cave walls and walking paths!

---

## ⚙️ How It Works & Methodology

The algorithms directory adheres strictly to object-oriented software engineering principles:

- **Abstraction (Abstract Base Class)**:
  - [`BaseGridGenerator`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/base.py) defines the contract that all map generators must follow.
  - Forces concrete subclasses to implement the `.generate()` method.
- **Reproducibility via Seeded PRNG**:
  - Seeds Python's standard `random` library with `seed`. Passing the exact same integer seed yields 100% deterministic, identical map outputs.
- **Cellular Automata (Moore Neighbourhood)**:
  - `PrototypeGridGenerator` uses an 8-neighbor cellular automata algorithm.
  - Border cells outside the grid boundary are evaluated as solid walls to keep caves enclosed.

---

## 📂 Files in This Directory

| File | Class / Component | Description |
| :--- | :--- | :--- |
| 📄 [`base.py`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/base.py) | `BaseGridGenerator` | Abstract Base Class (ABC) defining grid properties (`seed`, `width`, `height`) and abstract `generate()` contract. |
| 📄 [`prototype_gen.py`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/prototype_gen.py) | `PrototypeGridGenerator` | Cellular Automata cave generator implementation with configurable wall probability and smooth passes. |
| 📄 [`__init__.py`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/__init__.py) | Package Init | Exports `BaseGridGenerator` and `PrototypeGridGenerator` for clean imports. |

---

## 💻 Example Code Usage

```python
from backend.algorithms.prototype_gen import PrototypeGridGenerator

# Create a generator with seed=42, 20x20 size, 45% initial wall chance, 1 smooth pass
generator = PrototypeGridGenerator(seed=42, width=20, height=20, wall_probability=0.45, smooth_passes=1)

# Generate the 2D grid matrix (list of rows containing 0s and 1s)
grid = generator.generate()

print(f"Generated {len(grid)}x{len(grid[0])} grid!")
```
