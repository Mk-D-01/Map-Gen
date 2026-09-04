# 🎨 Backend Export Module — Image Exporter Engine

Welcome to the **Backend Export Module**! This directory turns raw grid matrices (0s and 1s) into high-resolution PNG image files.

---

## 🧒 Explain Like I'm 5 (ELI5)

> Imagine you have a giant grid of numbers on paper where `0` means white paper and `1` means black square:
>
> 1. The **Exporter Painter** (`PNGExporter`) takes your grid of numbers.
> 2. For every `1`, it paints a dark black square of 20×20 pixels.
> 3. For every `0`, it leaves a clean white square of 20×20 pixels.
> 4. Once done painting every square, it saves the drawing as a PNG image file or streams it straight to your web browser download!

---

## ⚙️ How It Works & Methodology

The export layer uses Pillow (PIL) for image rendering:

- **Abstract Exporter (`BaseExporter`)**:
  - Defines the interface contract (`export()` and `export_to_bytes()`).
  - Ensures future exporters (e.g. SVG exporter, Tilemap JSON exporter) can be seamlessly integrated.
- **In-Memory Streaming (`BytesIO`)**:
  - `PNGExporter.export_to_bytes()` renders the PNG directly into memory (`io.BytesIO`) without writing temporary files to disk.
  - This allows the Flask API (`/api/export`) to stream image downloads directly to users blazingly fast!
- **Configurable Aesthetics**:
  - Cell pixel dimensions (`cell_size`) and custom RGB colors (`wall_color`, `floor_color`) can be easily passed to the constructor.

---

## 📂 Files in This Directory

| File | Component | Description |
| :--- | :--- | :--- |
| 📄 [`base_exporter.py`](file:///e:/Projects/PBL/Map%20Gen/backend/export/base_exporter.py) | `BaseExporter` | Abstract Base Class defining file saving and in-memory byte streaming contracts. |
| 📄 [`prototype_export.py`](file:///e:/Projects/PBL/Map%20Gen/backend/export/prototype_export.py) | `PNGExporter` | Pillow-based exporter rendering 2D integer matrices into square-tiled PNG images. |
| 📄 [`__init__.py`](file:///e:/Projects/PBL/Map%20Gen/backend/export/__init__.py) | Package Init | Re-exports `BaseExporter` and `PNGExporter`. |

---

## 💻 Code Usage Example

```python
from backend.export.prototype_export import PNGExporter

matrix = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]

# Create exporter with cell_size of 30 pixels
exporter = PNGExporter(cell_size=30, wall_color=(40, 40, 40), floor_color=(220, 220, 220))

# Save directly to disk
output_file = exporter.export(matrix, "my_cave.png")
print(f"Saved PNG to {output_file}")
```
