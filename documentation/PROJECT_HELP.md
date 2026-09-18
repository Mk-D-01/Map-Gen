# 💡 MapGen Engine — Project Help & Quick Reference

This guide provides operational instructions, command-line usage, and development guidelines for MapGen Engine.

---

## ⚡ Quick Start Commands

### 1. Environment Setup
Make sure Python 3.9+ is installed. Activate your virtual environment and install dependencies:
```bash
# Create and activate virtual environment (Windows PowerShell)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Flask Backend API
```bash
python backend/app.py
```
- Server starts on `http://127.0.0.1:5000`
- Endpoints:
  - `GET /health` — Check server status
  - `POST /api/generate` — Generate procedural grid matrix
  - `POST /api/export` — Stream PNG image directly in-memory

### 3. Run Bitmask Autotiler Tool
```bash
python bitmask/app.py
```
- Navigate to `http://127.0.0.1:5000` in your browser to test interactive tile slicing, bitmask assignment, and procedural level generation.

### 4. Run Automated Pytest Harness
```bash
pytest tests/ -v
```

---

## 🛠️ Shifting Operations to Native C / C++

To shift computational operations (smoothing, bitmasks, BFS cavity cleanup, noise) to native speed:

### 1. Compile `mapgen_core.c` into a Dynamic Shared Library:
```bash
# Windows (MinGW / GCC):
gcc -O3 -shared -o backend/native/mapgen_core.dll backend/native/mapgen_core.c

# Windows (MSVC Developer Command Prompt):
cl /LD /O2 backend\native\mapgen_core.c /Fe:backend\native\mapgen_core.dll

# Linux / macOS:
gcc -O3 -shared -fPIC -o backend/native/mapgen_core.so backend/native/mapgen_core.c

# Browser WebAssembly (Zero-Latency Client Shift via Emscripten):
emcc -O3 backend/native/mapgen_core.c -s WASM=1 -o frontend/static/js/mapgen_wasm.js
```

### 2. Operations Shifted:
- **Operation 1: `generate_cave_c()`** — Random seed fill and Moore-neighborhood 4-5 smoothing.
- **Operation 2: `calculate_bitmasks_c()`** — Vectorized full-grid 4-bit autotiling resolution ($0 \dots 15$).
- **Operation 3: `prune_isolated_caves_c()`** — In-place BFS flood-fill eliminating unreachable cave pockets.
- **Operation 4: `generate_noise_c()`** — Multi-octave continuous noise with Hermite curves and SIMD registers.

### 3. How Python Calls Shifted Operations:
```python
from backend.algorithms.c_bridge import generate_cave_pipeline
# One-line execution of C generation + pruning + bitmasking:
result = generate_cave_pipeline(seed=42, width=64, height=64)
# result["grid"]  -> 2D level matrix (0 = floor, 1 = wall)
# result["masks"] -> 2D autotiling bitmasks (0-15)
```

---

## 🎯 Dual-Mode Flow Reference

### Case A: Preconfigured Assets (Quick Generation)
1. Select preset theme (e.g. *Dungeon Ruins*, *Caverns*, *Overworld*).
2. The system automatically loads pre-mapped 16-state bitmask coordinates from `backend/presets/`.
3. Set seed & grid dimensions $\to$ click **Generate**.
4. Map renders directly with no manual mapping required.

### Case B: Custom Asset Upload & Bitmask Studio
1. Upload custom spritesheet image (PNG/JPG).
2. Input tile width and height (e.g. 16, 32, 64 pixels).
3. Select bitmask value ($0 \dots 15$) and click the matching tile on the spritesheet canvas.
4. Export or save the mapping dictionary JSON.
5. Click **Generate Map** to produce procedural levels with your custom tiles.

---

## 📚 Related Documentation Links
- Main Architecture & DSA Manual: [`documentation/README.md`](file:///e:/Projects/PBL/Map%20Gen/documentation/README.md)
- PBL Academic Progress Report: [`collageRequirement/PROJECT_REPORT_SHEET.md`](file:///e:/Projects/PBL/Map%20Gen/collageRequirement/PROJECT_REPORT_SHEET.md)
- C Prototype Source Code: [`previousStack/map_gen_1.c`](file:///e:/Projects/PBL/Map%20Gen/previousStack/map_gen_1.c)
