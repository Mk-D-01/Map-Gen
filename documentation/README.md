# 🗺️ MapGen Engine — Comprehensive Architecture & Project Guide

**Course / Module:** Problem-Based Learning (PBL)  
**Project Title:** MapGen Engine — Procedural Map Generator Platform  
**Document Purpose:** System Documentation, Technical Overview, Data Structures Analysis, C/C++ Integration Guide, and Dual-Mode Workflow Reference.

---

## 📋 Table of Contents
1. [Project Overview & Problem Statement](#1-project-overview--problem-statement)
2. [Current Capabilities & What the Project Does Till Now](#2-current-capabilities--what-the-project-does-till-now)
3. [Comprehensive Data Structures Analysis (DSA)](#3-comprehensive-data-structures-analysis-dsa)
4. [Porting Algorithms to C / C++ While Maintaining Compatibility](#4-porting-algorithms-to-c--c-while-maintaining-compatibility)
5. [Program Workflow: Preconfigured vs. Custom Asset Bitmasking](#5-program-workflow-preconfigured-vs-custom-asset-bitmasking)
6. [Proposed System Directory Structure](#6-proposed-system-directory-structure)
7. [Step-by-Step Implementation Roadmap](#7-step-by-step-implementation-roadmap)

---

## 1. Project Overview & Problem Statement

### 1.1 Project Summary
**MapGen Engine** is an open-source, full-stack procedural content generation (PCG) platform designed to synthesize 2D grid-based environments (caves, dungeons, and natural terrain) deterministically. The engine uses mathematical algorithms to turn an integer random seed into structured level layouts with zero manual level design overhead.

### 1.2 Problem Statement
In modern game development and spatial simulation, designing levels manually is labor-intensive and limits replayability. Procedural content generation addresses this, but introduces three academic challenges:
1. **Seed Determinism:** The exact same integer seed must consistently generate the identical map matrix across client and server environments.
2. **Algorithmic Efficiency & Space Partitioning:** Partitioning large grids while ensuring memory safety, low latency, and guaranteed traversability.
3. **Interactive Visual Diagnostics:** Giving developers and designers visual evaluation tools to inspect, tweak, and export maps and tile bitmasks in real-time.

---

## 2. Current Capabilities & What the Project Does Till Now

The project has achieved its **Phase 1 Operational Milestone**:

```
+-----------------------------------------------------------------------------------+
|                            SYSTEM ARCHITECTURE                                    |
|                                                                                   |
|  [ Interactive Web Visualizers ]  <--->  [ Python Flask REST API ]                |
|    - HTML5 Canvas Sandboxes                - /api/generate & /api/export          |
|    - Algorithm parameter sliders           - Factory & Strategy OOP Patterns      |
|    - PNG & JSON Matrix download            - In-memory Pillow PNG streaming       |
|                                                     |                             |
|                                                     v                             |
|                                         [ Core Procedural Engine ]                |
|                                           - Cellular Automata (Caves)             |
|                                           - BSP Tree (Dungeons)                   |
|                                           - Perlin/Smooth Noise (Biomes)          |
|                                           - Bitmask Autotiling                    |
+-----------------------------------------------------------------------------------+
```

### Key Modules Implemented:
1. **Cellular Automata Cave Generation (`backend/algorithms/prototype_gen.py`, `web/cellular.html`):**
   - Configurable initial wall probability fill (default 45%).
   - Iterative smoothing passes using a 4-5 voting rule over an 8-neighbor Moore neighborhood.
2. **Binary Space Partitioning (BSP) Dungeons (`web/bsp.html`, `web/bsp-tree.html`):**
   - Recursive bisection of 2D bounding boxes into sub-quadrants.
   - Room carving within leaf nodes and corridor centroid linking.
3. **Perlin & Smooth Value Noise (`web/perlin.html`, `previousStack/map_gen_1.c`):**
   - Multi-octave continuous gradient noise with Hermite quintic fade curves and linear interpolation (`Lerp`).
   - Generates natural terrain heightmaps classified into biomes (Water, Sand, Meadow, Forest).
4. **Interactive Tile Bitmask Autotiling (`bitmask/app.py`, `bitmask/templates/index.html`):**
   - Evaluates 4-bit cardinal neighbor connectivity ($2^0=N, 2^1=E, 2^2=S, 2^3=W$) to map cells to values $0 \dots 15$.
   - Interactive canvas allowing designers to slice tiles and assign bitmask IDs.
5. **Cavity Cleanup via BFS Flood Fill (`web/app.js`):**
   - Traverses connected open floor spaces to isolate distinct cave regions.
   - Preserves the largest connected region and fills unreachable pockets with solid walls.
6. **Backend Flask REST API (`backend/app.py`):**
   - Object-Oriented design using Factory and Strategy patterns.
   - `POST /api/generate`: Returns JSON map matrix.
   - `POST /api/export`: Direct in-memory rasterization to PNG via Pillow and `io.BytesIO`.
7. **Automated Test Suite (`tests/test_prototype.py`):**
   - 10/10 passing tests verifying PRNG seed determinism, grid boundaries, HTTP codes, and PNG magic byte headers (`\x89PNG\r\n\x1a\n`).
8. **Legacy C Prototypes (`previousStack/`):**
   - Compiled C prototypes proving computational execution speed and memory efficiency.

---

## 3. Comprehensive Data Structures Analysis (DSA)

The engine leverages six primary data structures:

| Data Structure | Implementation Location | Purpose | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **1. 2D Spatial Grid / Flattened 1D Buffer** | `backend/algorithms/`, `web/spatial-grid.html` | Tile storage, matrix access | $O(1)$ lookup | $O(W \times H)$ |
| **2. Binary Tree (BSP Tree)** | `web/app.js`, `web/bsp-tree.html` | Dungeon space partitioning | $O(N \log N)$ build | $O(N)$ nodes |
| **3. Moore & Von Neumann Neighborhoods** | `backend/algorithms/`, `web/moore-neighborhood.html` | Convolution stencil sampling | $O(1)$ per cell | $O(1)$ |
| **4. FIFO Queue & Hash Set (BFS)** | `web/app.js` | Cave cavity cleanup & connectivity | $O(W \times H)$ | $O(W \times H)$ |
| **5. Spatial Bitwise Hash Function** | `web/app.js`, `web/spatial-hash.html` | Stateless PRNG lookup table | $O(1)$ bitwise | $O(1)$ (0 bytes) |
| **6. 4-bit Bitmask Vector** | `bitmask/app.py` | Autotiling sprite selection | $O(1)$ bitwise | $O(1)$ |

### In-Depth Mathematical & Architectural Details:

#### 1. 2D Spatial Grid & Flattened 1D Matrix Buffer
- Converts 2D $(x, y)$ coordinate pairs into a contiguous 1D array in row-major order:
  $$\text{Index}(x, y) = y \cdot \text{Width} + x$$
  $$\text{Inverse: } x = i \pmod{\text{Width}}, \quad y = \lfloor i / \text{Width} \rfloor$$
- **Benefit:** Eliminates pointer indirection in nested arrays and ensures CPU cache-line alignment during sequential grid sweeps.

#### 2. Binary Space Partitioning (BSP) Tree
- Hierarchical binary tree where each node holds bounding bounds $(x, y, w, h)$.
- Interior nodes hold splitting planes (horizontal or vertical) and pointers to `leftChild` and `rightChild`.
- Leaf nodes hold final carved room dimensions and center coordinates (`cx, cy`). Corridors are generated by walking from sibling leaf centroids.

#### 3. Moore & Von Neumann Neighborhood Kernels
- **Moore Neighborhood ($N_8$):** Stencil covering 8 surrounding orthogonal + diagonal cells ($\max(|x - x'|, |y - y'|) = 1$, Chebyshev distance). Used in Cellular Automata cave smoothing.
- **Von Neumann Neighborhood ($N_4$):** Stencil covering 4 orthogonal cells ($|x - x'| + |y - y'| = 1$, Manhattan distance). Used in bitmasking and flood-fill connectivity.

#### 4. FIFO Queue & Hash Set (BFS Flood Fill)
- A queue `[{x, y}]` explores unvisited floor coordinates.
- Tracks disconnected cave cavities, computes area sizes, keeps the maximum component, and converts orphan spaces into solid walls.

#### 5. Spatial Bitwise Hash Function
- Stateless pseudo-random coordinate hashing function:
  $$n = (x + y \cdot 57 + \text{seed} \cdot 131) \ll 13 \oplus n$$
  $$\text{Hash} = 1.0 - \frac{((n \cdot (n^2 \cdot 15731 + 789221) + 1376312589) \ \& \ \text{0x7FFFFFFF})}{1073741824.0}$$
- Eliminates state tracking found in linear PRNGs, enabling out-of-order coordinate queries in $O(1)$ with 0 bytes memory overhead.

#### 6. 4-Bit Bitmask Autotiling Vector
- Packs 4 cardinal neighbor states into a single nibble ($0 \dots 15$):
  ```python
  mask = 0
  if north_is_terrain: mask |= 1  # 2^0
  if east_is_terrain:  mask |= 2  # 2^1
  if south_is_terrain: mask |= 4  # 2^2
  if west_is_terrain:  mask |= 8  # 2^3
  ```
- Enables instant lookup for the matching border, corner, or center sprite.

---

## 4. Porting Algorithms to C / C++ While Maintaining Compatibility

To achieve native C/C++ execution performance without disrupting the Python Flask server or web frontend, compile the algorithms into a dynamic shared library (`.dll` on Windows, `.so` on Linux) and invoke them from Python using `ctypes`.

### Step 1: Write the C Core (`backend/native/mapgen.c`)
### 4.1 Architectural Strategy: The "Zero-Copy Flattened Buffer Pattern"
In Python and JavaScript, iterating through nested matrices (`grid[y][x]`) causes massive CPU cache misses, pointer indirection, and garbage-collector overhead. 

To shift heavy computational operations to C/C++:
1. **Allocate in Caller (Python/JS):** A single contiguous 1D memory buffer (`uint8_t` or `int32_t`) of size $\text{Width} \times \text{Height}$ is allocated.
2. **Pass Pointer to C/C++:** Python passes the raw memory pointer (`ctypes.POINTER(ctypes.c_uint8)`) directly across the FFI (Foreign Function Interface) boundary.
3. **In-Place Native Execution:** C/C++ operates directly on the contiguous buffer using pointer arithmetic and integer indexing (`y * width + x`).
4. **Zero-Copy Consumption:** Python converts the populated buffer into Python lists or NumPy arrays for JSON serialization, or directly passes bytes to Pillow for PNG streaming.

---

### 4.2 The Four Operations Shifted to C/C++

#### ⚙️ Operation 1: Cellular Automata Cave Generation & Smoothing
- **What is shifted:** Random filling, solid border generation, and iterative Moore-neighborhood convolution passes (4-5 voting rule).
- **C Performance Gain:** $15\times$ to $50\times$ faster than nested Python `for` loops.

#### ⚙️ Operation 2: Grid-Wide Bitmask Autotiling Calculation
- **What is shifted:** For every cell $(x, y)$, evaluating North, East, South, West neighbors and computing the 4-bit integer mask ($0 \dots 15$):
  $$\text{mask} = (N \cdot 1) \ | \ (E \cdot 2) \ | \ (S \cdot 4) \ | \ (W \cdot 8)$$
- **C Performance Gain:** Vectorized integer bitwise operations run in a single contiguous memory sweep.

#### ⚙️ Operation 3: BFS Flood Fill & Cave Cavity Pruning
- **What is shifted:** Breadth-First Search flood-fill traversing open floor spaces to identify disconnected cave components, calculate areas, preserve the largest playable cave, and fill isolated pockets with solid walls.
- **C Performance Gain:** Uses a fast static array queue instead of Python objects and set hashing, eliminating heap allocations.

#### ⚙️ Operation 4: 2D Multi-Octave Continuous Noise (Biomes & Terrains)
- **What is shifted:** Bitwise coordinate hashing, quintic Hermite fade curves ($6t^5 - 15t^4 + 10t^3$), linear interpolation (`Lerp`), and octave accumulation.
- **C Performance Gain:** Floating-point math utilizes CPU SIMD and hardware registers.

---

### 4.3 Unified C Core Implementation (`backend/native/mapgen_core.c`)

Here is the complete C source code implementing all shifted operations:

```c
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <math.h>

#if defined(_WIN32)
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

/* =========================================================================
   OPERATION 1: Cellular Automata Cave Generation
   ========================================================================= */
EXPORT void generate_cave_c(int seed, int width, int height, float fill_prob, int smooth_passes, uint8_t* out_grid) {
    srand(seed);
    int total = width * height;

    // 1. Initial random distribution with solid border
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int idx = y * width + x;
            if (x == 0 || x == width - 1 || y == 0 || y == height - 1) {
                out_grid[idx] = 1; // Solid border
            } else {
                out_grid[idx] = (((float)rand() / (float)RAND_MAX) < fill_prob) ? 1 : 0;
            }
        }
    }

    // 2. Iterative smoothing passes (Moore 4-5 rule)
    uint8_t* temp = (uint8_t*)malloc(total);
    for (int p = 0; p < smooth_passes; p++) {
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int idx = y * width + x;
                if (x == 0 || x == width - 1 || y == 0 || y == height - 1) {
                    temp[idx] = 1;
                    continue;
                }
                int wall_count = 0;
                for (int dy = -1; dy <= 1; dy++) {
                    for (int dx = -1; dx <= 1; dx++) {
                        if (dx == 0 && dy == 0) continue;
                        wall_count += out_grid[(y + dy) * width + (x + dx)];
                    }
                }
                // Standard 4-5 rule with hysteresis
                if (wall_count > 4) temp[idx] = 1;
                else if (wall_count < 4) temp[idx] = 0;
                else temp[idx] = out_grid[idx];
            }
        }
        for (int i = 0; i < total; i++) out_grid[i] = temp[i];
    }
    free(temp);
}

/* =========================================================================
   OPERATION 2: Full-Grid Autotiling Bitmask Resolution
   Computes 4-bit mask (0-15) for every cell: N(1), E(2), S(4), W(8)
   ========================================================================= */
EXPORT void calculate_bitmasks_c(const uint8_t* grid, int width, int height, uint8_t* out_masks) {
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int idx = y * width + x;
            if (grid[idx] == 0) {
                out_masks[idx] = 0xFF; // Sentinel 255 indicates empty / water cell
                continue;
            }

            uint8_t mask = 0;
            if (y > 0 && grid[(y - 1) * width + x] == 1)          mask |= 1; // North
            if (x < width - 1 && grid[y * width + (x + 1)] == 1)  mask |= 2; // East
            if (y < height - 1 && grid[(y + 1) * width + x] == 1) mask |= 4; // South
            if (x > 0 && grid[y * width + (x - 1)] == 1)          mask |= 8; // West

            out_masks[idx] = mask;
        }
    }
}

/* =========================================================================
   OPERATION 3: BFS Flood Fill Cave Pocket Pruning
   Isolates distinct open floor regions and fills unplayable pockets
   ========================================================================= */
EXPORT void prune_isolated_caves_c(uint8_t* grid, int width, int height) {
    int total = width * height;
    bool* visited = (bool*)calloc(total, sizeof(bool));
    int* qx = (int*)malloc(total * sizeof(int));
    int* qy = (int*)malloc(total * sizeof(int));

    int max_cave_size = 0;
    int max_cave_start_idx = -1;

    // Scan grid to find the largest connected open floor region
    for (int y = 1; y < height - 1; y++) {
        for (int x = 1; x < width - 1; x++) {
            int start_idx = y * width + x;
            if (grid[start_idx] == 0 && !visited[start_idx]) {
                int q_head = 0, q_tail = 0;
                qx[q_tail] = x; qy[q_tail] = y; q_tail++;
                visited[start_idx] = true;
                int current_size = 0;

                while (q_head < q_tail) {
                    int cx = qx[q_head]; int cy = qy[q_head]; q_head++;
                    current_size++;

                    int dxs[] = { 0, 1, 0, -1 };
                    int dys[] = { -1, 0, 1, 0 };
                    for (int d = 0; d < 4; d++) {
                        int nx = cx + dxs[d];
                        int ny = cy + dys[d];
                        if (nx > 0 && nx < width - 1 && ny > 0 && ny < height - 1) {
                            int nidx = ny * width + nx;
                            if (grid[nidx] == 0 && !visited[nidx]) {
                                visited[nidx] = true;
                                qx[q_tail] = nx; qy[q_tail] = ny; q_tail++;
                            }
                        }
                    }
                }

                if (current_size > max_cave_size) {
                    max_cave_size = current_size;
                    max_cave_start_idx = start_idx;
                }
            }
        }
    }

    // Second pass: Mark all floor cells except those in the largest cave as walls
    if (max_cave_start_idx != -1) {
        for (int i = 0; i < total; i++) visited[i] = false;
        int q_head = 0, q_tail = 0;
        int sx = max_cave_start_idx % width;
        int sy = max_cave_start_idx / width;
        qx[q_tail] = sx; qy[q_tail] = sy; q_tail++;
        visited[max_cave_start_idx] = true;

        while (q_head < q_tail) {
            int cx = qx[q_head]; int cy = qy[q_head]; q_head++;
            int dxs[] = { 0, 1, 0, -1 };
            int dys[] = { -1, 0, 1, 0 };
            for (int d = 0; d < 4; d++) {
                int nx = cx + dxs[d];
                int ny = cy + dys[d];
                if (nx > 0 && nx < width - 1 && ny > 0 && ny < height - 1) {
                    int nidx = ny * width + nx;
                    if (grid[nidx] == 0 && !visited[nidx]) {
                        visited[nidx] = true;
                        qx[q_tail] = nx; qy[q_tail] = ny; q_tail++;
                    }
                }
            }
        }

        // Fill non-visited floor cells with wall (1)
        for (int i = 0; i < total; i++) {
            if (grid[i] == 0 && !visited[i]) {
                grid[i] = 1;
            }
        }
    }

    free(visited);
    free(qx);
    free(qy);
}

/* =========================================================================
   OPERATION 4: Smooth Value Noise (Terrain & Biomes)
   ========================================================================= */
static inline float hash_coord(int x, int y, int seed) {
    int n = x + y * 57 + seed * 131;
    n = (n << 13) ^ n;
    return 1.0f - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0f;
}

static inline float smooth_fade(float t) {
    return t * t * t * (t * (t * 6.0f - 15.0f) + 10.0f);
}

static inline float lerp_val(float a, float b, float t) {
    return a + t * (b - a);
}

EXPORT void generate_noise_c(int seed, int width, int height, float scale, int octaves, float roughness, float* out_heightmap) {
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            float n = 0.0f;
            float freq = scale;
            float amp = 1.0f;
            float max_amp = 0.0f;

            for (int o = 0; o < octaves; o++) {
                float sx = x * freq;
                float sy = y * freq;
                int X = (int)floorf(sx);
                int Y = (int)floorf(sy);
                float xf = sx - floorf(sx);
                float yf = sy - floorf(sy);

                float u = smooth_fade(xf);
                float v = smooth_fade(yf);

                float n00 = (hash_coord(X, Y, seed + o * 100) + 1.0f) * 0.5f;
                float n10 = (hash_coord(X + 1, Y, seed + o * 100) + 1.0f) * 0.5f;
                float n01 = (hash_coord(X, Y + 1, seed + o * 100) + 1.0f) * 0.5f;
                float n11 = (hash_coord(X + 1, Y + 1, seed + o * 100) + 1.0f) * 0.5f;

                float x1 = lerp_val(n00, n10, u);
                float x2 = lerp_val(n01, n11, u);
                n += lerp_val(x1, x2, v) * amp;
                max_amp += amp;

                freq *= 2.0f;
                amp *= roughness;
            }

            out_heightmap[y * width + x] = n / max_amp;
        }
    }
}
```

---

### 4.4 Compiling the C Core to Dynamic Library

```bash
# Windows (MinGW GCC)
gcc -O3 -shared -o backend/native/mapgen_core.dll backend/native/mapgen_core.c

# Windows (MSVC Developer Shell)
cl /LD /O2 backend\native\mapgen_core.c /Fe:backend\native\mapgen_core.dll

# Linux / macOS
gcc -O3 -shared -fPIC -o backend/native/mapgen_core.so backend/native/mapgen_core.c
```

---

### 4.5 Python `ctypes` Bridge Layer (`backend/algorithms/c_bridge.py`)

This module exposes clean, idiomatic Python functions while delegating execution to the compiled C engine:

```python
from __future__ import annotations
import ctypes
import os
import sys

_lib_name = "mapgen_core.dll" if sys.platform == "win32" else "mapgen_core.so"
_lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "native", _lib_name))

HAS_C_ENGINE = False
try:
    _c_lib = ctypes.CDLL(_lib_path)

    # 1. generate_cave_c signature
    _c_lib.generate_cave_c.argtypes = [
        ctypes.c_int, ctypes.c_int, ctypes.c_int,
        ctypes.c_float, ctypes.c_int,
        ctypes.POINTER(ctypes.c_uint8)
    ]

    # 2. calculate_bitmasks_c signature
    _c_lib.calculate_bitmasks_c.argtypes = [
        ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int,
        ctypes.POINTER(ctypes.c_uint8)
    ]

    # 3. prune_isolated_caves_c signature
    _c_lib.prune_isolated_caves_c.argtypes = [
        ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int
    ]

    # 4. generate_noise_c signature
    _c_lib.generate_noise_c.argtypes = [
        ctypes.c_int, ctypes.c_int, ctypes.c_int,
        ctypes.c_float, ctypes.c_int, ctypes.c_float,
        ctypes.POINTER(ctypes.c_float)
    ]
    HAS_C_ENGINE = True
except Exception as err:
    print(f"⚠️ Native C engine unavailable, using Python fallback: {err}")


def generate_cave_pipeline(seed: int, width: int, height: int, fill_prob: float = 0.45, smooth_passes: int = 4, prune: bool = True):
    """Executes the complete C generation + pruning + bitmask pipeline in a single pass."""
    total = width * height
    grid_buffer = (ctypes.c_uint8 * total)()
    mask_buffer = (ctypes.c_uint8 * total)()

    # Run C generation
    _c_lib.generate_cave_c(seed, width, height, fill_prob, smooth_passes, grid_buffer)

    # Run C cave pocket pruning
    if prune:
        _c_lib.prune_isolated_caves_c(grid_buffer, width, height)

    # Run C full-grid bitmask calculation
    _c_lib.calculate_bitmasks_c(grid_buffer, width, height, mask_buffer)

    raw_grid = list(grid_buffer)
    raw_masks = list(mask_buffer)

    # Reshape into 2D structures for Flask JSON response
    grid_2d = [raw_grid[y * width : (y + 1) * width] for y in range(height)]
    masks_2d = [
        [None if raw_masks[y * width + x] == 255 else raw_masks[y * width + x] for x in range(width)]
        for y in range(height)
    ]

    return {"grid": grid_2d, "masks": masks_2d}
```

---

### 4.6 Alternative Browser Shift: WebAssembly (WASM via Emscripten)
If you want operations to execute **directly in the user's web browser** with zero network latency and zero server CPU usage:

1. Install [Emscripten SDK](https://emscripten.org/).
2. Compile `mapgen_core.c` to WebAssembly:
   ```bash
   emcc -O3 backend/native/mapgen_core.c -s WASM=1 -s EXPORTED_FUNCTIONS="['_generate_cave_c', '_calculate_bitmasks_c']" -o frontend/static/js/mapgen_wasm.js
   ```
3. Call it directly inside `frontend/static/js/app.js` via `Module._generate_cave_c(...)`.


---

## 5. Program Workflow: Preconfigured vs. Custom Asset Bitmasking

The application handles two distinct user journeys:

```
                                  [ User Lands on App ]
                                             │
                       ┌─────────────────────┴─────────────────────┐
                       ▼                                           ▼
             [ CASE A: PRECONFIGURED ]                   [ CASE B: CUSTOM ASSETS ]
                       │                                           │
         Choose Preset: Cave / Dungeon / Forest           Upload Spritesheet Image
                       │                                           │
         Pre-defined Bitmask JSON Loaded               Interactive Bitmask Studio (0-15)
                       │                               - User clicks sprite for each mask
                       │                               - Saves or exports Mapping JSON
                       └─────────────────────┬─────────────────────┘
                                             │
                                             ▼
                             [ Configure Generation Params ]
                               (Seed, WxH, Algorithm)
                                             │
                                             ▼
                             [ C/C++ Procedural Generator ]
                               (Produces Binary Grid 0/1)
                                             │
                                             ▼
                              [ Bitmask Resolution Engine ]
                           (Computes 4-bit mask for each cell)
                                             │
                                             ▼
                              [ HTML5 Canvas Level Renderer ]
                           (Draws crop rects from spritesheet)
                                             │
                                             ▼
                               [ Export: PNG / JSON / CSV ]
```

### 5.1 Case A: User Uses Preconfigured Assets
1. **Selection:** User selects a preset theme from a dropdown:
   - 🏰 **Dungeon Ruins** (BSP algorithm + dungeon tileset)
   - 🪨 **Deep Caverns** (Cellular Automata + stone cave tileset)
   - 🌲 **Overworld Biome** (Perlin Noise + grass/water tileset)
2. **Bundled Asset & Mapping:**
   - Pre-mapped JSON files (`backend/presets/dungeon_mapping.json`) contain crop rectangles for all 16 bitmask states.
3. **Instant Rendering:**
   - The user clicks **Generate**. C/C++ engine runs, cell bitmasks are resolved, and the canvas renders the level immediately.

### 5.2 Case B: User Uploads Custom Asset Spritesheet
1. **Upload & Slicing:**
   - User uploads their custom spritesheet (PNG/JPG).
   - User defines tile dimensions (e.g. 16×16, 32×32, or 64×64).
   - The system displays the sheet in an interactive canvas with a grid overlay.
2. **Interactive Bitmask Assignment (0 to 15):**
   - The UI displays a reference selector showing the 16 cardinal connection states:
     ```
     0: Isolated single tile (no neighbors)
     1: North end only
     2: East end only
     3: North + East corner
     ...
     15: Center tile (surrounded by N, E, S, W)
     ```
   - The user clicks a tile on their sheet to bind it to a bitmask ID:
     ```json
     "15": { "x": 128, "y": 64, "w": 32, "h": 32 }
     ```
   - **Fallback Mechanism:** Unassigned bitmasks fall back to default solid colored tiles so the map remains fully renderable.
   - User can **Export / Import Mapping JSON** to save their mapping configuration.
3. **Generation:**
   - Procedural engine produces the matrix, maps coordinates through the custom bitmask dictionary, and renders the level on canvas.

---

## 6. Proposed System Directory Structure

```
Map Gen/
├── backend/
│   ├── native/                        # <-- C/C++ Core Engine
│   │   ├── mapgen.c                   # Procedural generation source
│   │   ├── mapgen.h
│   │   └── mapgen.dll / mapgen.so     # Compiled native library
│   ├── algorithms/
│   │   ├── base.py                    # Abstract base classes
│   │   ├── c_bridge.py                # ctypes bridge to native library
│   │   └── prototype_gen.py           # Python generator & fallback
│   ├── presets/                       # <-- Case A Preconfigured Mappings
│   │   ├── dungeon_preset.json
│   │   ├── cave_preset.json
│   │   └── overworld_preset.json
│   ├── export/
│   │   └── prototype_export.py        # In-memory Pillow PNG streamer
│   └── app.py                         # Flask REST API server
│
├── frontend/                          # Unified Frontend Web Application
│   ├── static/
│   │   ├── presets/                   # Bundled tilesheet assets
│   │   │   ├── dungeon_tiles.png
│   │   │   └── cave_tiles.png
│   │   ├── js/
│   │   │   ├── bitmask_studio.js      # Case B custom upload & assignment
│   │   │   ├── level_renderer.js      # Canvas tilemap rendering
│   │   │   └── app.js                 # API bindings & UI controllers
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       └── index.html                 # Unified multi-tab web application
│
├── documentation/
│   ├── README.md                      # This comprehensive architecture document
│   └── PROJECT_HELP.md                # Quick-start setup & CLI cheat sheet
│
├── previousStack/                     # Legacy C implementations & benchmarks
├── tests/                             # Automated Pytest suite
└── requirements.txt
```

---

## 7. Step-by-Step Implementation Roadmap

1. **Step 1: Native C Engine Compilation**
   - Place `mapgen.c` under `backend/native/`.
   - Compile to `mapgen.dll` (Windows) using MinGW or MSVC.

2. **Step 2: Connect Python `ctypes` Bridge**
   - Create `backend/algorithms/c_bridge.py`.
   - Update `backend/app.py` `/api/generate` route to use `c_bridge.py` with seamless fallback to `prototype_gen.py`.

3. **Step 3: Export Default Presets (Case A)**
   - Bundle `Tilemap_color2.png` and save its completed 16-mask JSON as `backend/presets/dungeon_preset.json`.

4. **Step 4: Unified UI (Case A + Case B)**
   - Combine `bitmask/templates/index.html` with `web/index.html`.
   - Provide a tab or switch:
     - **Tab 1: Quick Generate (Case A)** $\to$ pick preset, choose seed, click Generate.
     - **Tab 2: Custom Bitmask Studio (Case B)** $\to$ upload image, slice tiles, bind masks 0–15, save JSON, and generate.

5. **Step 5: Export Capabilities**
   - Support downloads in multiple formats: PNG image, raw JSON matrix, and Tiled-compatible CSV.
