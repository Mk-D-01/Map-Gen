# 🧠 Algorithm Designer Role Guide — Procedural Map Engine

**Role**: Procedural Algorithm Designer  
**Scope**: Cellular Automata Algorithms, Seed Determinism, Neighbor Smoothing, Base Generator Contracts  
**Primary Directory**: [`backend/algorithms/`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/ALGORITHM_DESIGNER_ROLE.md)

---

## 🔬 How It Works Under the Hood

The algorithms module generates procedural grid layouts using object-oriented Python classes, seeded pseudo-random generation, and Cellular Automata smoothing passes.

```
1. Seed Initialization          2. Random Fill (45% Walls)          3. 8-Neighbor Smoothing Pass
+-----------------------+      +--------------------------+      +------------------------------+
| random.seed(seed=42)  | ---> |  [1, 0, 1, 1, 0, 0, 1]   | ---> |  Smooths isolated noise into |
| (Guarantees same map) |      |  [0, 1, 0, 1, 1, 0, 0]   |      |  connected cave caverns!     |
+-----------------------+      +--------------------------+      +------------------------------+
```

### 1. Abstract Base Class (`BaseGridGenerator`)
- Located in [`base.py`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/base.py).
- Defines the required template for all map generation algorithms.
- Enforces consistent parameters (`seed`, `width`, `height`) and ensures every generator implements a standard `.generate()` method.

### 2. Cellular Automata Cave Generation (`PrototypeGridGenerator`)
Located in [`prototype_gen.py`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/prototype_gen.py), the cave generator follows a 3-step process:

1. **Deterministic Seeding**:
   Calls `random.seed(seed)` before starting. This guarantees that running the algorithm with the exact same seed will always produce identical maps.
2. **Random Grid Initialization**:
   Fills the 2D grid matrix with `1`s (walls) and `0`s (floors) based on a configured `wall_probability` (default: 45%).
3. **8-Neighbor Smoothing Pass**:
   - For every cell, the algorithm inspects its 8 neighboring cells (up, down, left, right, and 4 diagonals).
   - Any cell outside the grid boundary is treated as a solid wall (`1`) to keep the cave enclosed.
   - If 5 or more neighbors are walls, the target cell becomes a wall (`1`). Otherwise, it becomes a floor (`0`).
   - Running this smoothing pass groups scattered random tiles into natural, connected cave systems.

---

## 📂 Subsystem File Overview

| File | Symbol | Purpose |
| :--- | :--- | :--- |
| 📄 [`base.py`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/base.py) | `BaseGridGenerator` | Abstract Base Class defining standard grid attributes and `.generate()` contract. |
| 📄 [`prototype_gen.py`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/prototype_gen.py) | `PrototypeGridGenerator` | Concrete Cellular Automata implementation for cave map generation. |
| 📄 [`__init__.py`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/__init__.py) | Package File | Exposes algorithm classes for clean module imports. |

---

## 💻 Python Code Usage Example

```python
from backend.algorithms.prototype_gen import PrototypeGridGenerator

# Create a generator instance (Seed: 42, Size: 20x20, Wall Fill: 45%)
generator = PrototypeGridGenerator(seed=42, width=20, height=20, wall_probability=0.45, smooth_passes=1)

# Generate the 2D matrix (list of rows containing 0s and 1s)
grid = generator.generate()

print(f"Generated a {len(grid)}x{len(grid[0])} cave map matrix!")
```
