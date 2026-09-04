# 🎨 Graphics Exporter Role Guide — Image Rasterization Engine

**Role**: Graphics & Exporter Subsystem Engineer  
**Scope**: Pillow (PIL) Image Rasterization, Base Exporter Contracts, RGB Palette Customization, BytesIO Streaming  
**Primary Directory**: [`backend/export/`](file:///e:/Projects/PBL/Map%20Gen/backend/export/EXPORTER_ENGINEER_ROLE.md)

---

## 🔬 How It Works Under the Hood

The export module turns 2D grid matrices (arrays of `0`s and `1`s) into high-resolution PNG image files using Python's Pillow (PIL) library.

```
 2D Grid Matrix                        Pillow PNG Rasterizer                    Image Output
+---------------+                     +----------------------+                 +--------------------+
| [[1, 1, 1],   |  -----------------> | PNGExporter          | --------------> | File: map.png      |
|  [1, 0, 1],   |                     | - Paints Wall Tiles  |                 | OR                 |
|  [1, 1, 1]]   |                     | - Paints Floor Tiles |                 | In-Memory Stream   |
+---------------+                     +----------------------+                 +--------------------+
```

### 1. Abstract Base Class (`BaseExporter`)
- Located in [`base_exporter.py`](file:///e:/Projects/PBL/Map%20Gen/backend/export/base_exporter.py).
- Establishes a standard contract for exporting map matrices, defining required methods for both direct file output (`export`) and in-memory byte streaming (`export_to_bytes`).

### 2. PNG Rasterization Engine (`PNGExporter`)
Located in [`prototype_export.py`](file:///e:/Projects/PBL/Map%20Gen/backend/export/prototype_export.py):

1. **Canvas Sizing**:
   Calculates total image dimensions based on grid size and cell pixel scale:
   $$\text{Image Width} = \text{Grid Width} \times \text{Cell Pixel Size}$$
   $$\text{Image Height} = \text{Grid Height} \times \text{Cell Pixel Size}$$
2. **Tile Painting**:
   - Creates a new RGB image surface with the designated floor background color.
   - Loops through every cell in the 2D matrix. For each `1` (wall), draws a filled rectangle using the designated wall color.
3. **In-Memory Binary Streaming (`io.BytesIO`)**:
   - `export_to_bytes()` renders the PNG directly into memory (`io.BytesIO`) instead of writing temporary files to disk.
   - This allows the Flask server (`/api/export`) to stream image downloads directly to web browsers blazingly fast.

---

## 📂 Subsystem File Overview

| File | Class / Symbol | Purpose |
| :--- | :--- | :--- |
| 📄 [`base_exporter.py`](file:///e:/Projects/PBL/Map%20Gen/backend/export/base_exporter.py) | `BaseExporter` | Abstract Base Class defining file saving and byte streaming contracts. |
| 📄 [`prototype_export.py`](file:///e:/Projects/PBL/Map%20Gen/backend/export/prototype_export.py) | `PNGExporter` | Pillow-based exporter rendering 2D grid matrices into PNG image files or byte streams. |
| 📄 [`__init__.py`](file:///e:/Projects/PBL/Map%20Gen/backend/export/__init__.py) | Package File | Exposes exporter classes for clean imports. |

---

## 💻 Python Code Usage Example

```python
from backend.export.prototype_export import PNGExporter

matrix = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]

# Create exporter with cell size of 20 pixels
exporter = PNGExporter(cell_size=20, wall_color=(30, 30, 46), floor_color=(137, 180, 250))

# Save image directly to disk
exporter.export(matrix, "cave_map.png")
```
