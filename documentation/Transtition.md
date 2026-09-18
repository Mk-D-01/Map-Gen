# Transitioning to C/C++ While Keeping the Project Compatible

## 1. Objective

This document explains how to move the heavy procedural generation logic from Python into C or C++ without breaking the current project structure or user experience.

The project is designed around a clean separation of responsibilities:

- Python handles user interaction, routing, orchestration, and export
- C/C++ handles computationally expensive operations
- the system still exposes the same API and output format to the rest of the project

The end goal is to improve performance while keeping the project compatible with:

- Flask REST API routes
- Streamlit or frontend web UI
- JSON map output
- PNG export
- preconfigured presets
- custom user tilesets and bitmask assignment

---

## 2. Why move algorithms to C/C++?

The procedural algorithms in this project work, but some of them are repeatedly executed over large grids and do expensive neighborhood checks, flood fills, and noise calculations. These operations are ideal candidates for native code because they are:

- computationally heavy
- deterministic
- independent of UI code
- easy to isolate behind a small Python interface

Typical high-cost operations include:

- Cellular automata smoothing
- BFS cavity cleanup
- BSP dungeon generation
- bitmask evaluation for autotiling
- Perlin/smooth noise map generation

Moving only the heavy kernels to native code gives the best performance-to-risk ratio.

---

## 3. Compatibility-first design principle

The key rule is:

> Keep the public project behavior the same, even when the internal algorithm runs in C/C++.

That means:

- same seed input should produce same output as before when configured the same way
- same API contract must remain stable
- same JSON matrix format sh    ould be returned
- same PNG export flow should still work
- frontend and backend should not need major redesigns

This is achieved by keeping the Python layer as the orchestrator and making the native layer a drop-in backend implementation.

---

## 4. Recommended transition pattern

### 4.1 Keep Python as the user-facing layer

Python should remain responsible for:

- receiving parameters from the user
- choosing the generation algorithm
- validating inputs
- building the response object
- exporting PNG or JSON output
- handling UI state

The native layer should only do the heavy calculations.

### 4.2 Expose native code behind a stable API

Instead of changing every file to direct C/C++ calls, create a compatibility layer such as:

- backend/algorithms/c_bridge.py
- backend/algorithms/native_engine.py
- backend/algorithms/factory.py

This layer should expose functions with the same names and parameter conventions as the current Python generator.

For example:

```python
# current Python style
result = generate_map(seed=42, width=64, height=64, algorithm="cave")

# native-compatible interface
result = engine.generate_map(seed=42, width=64, height=64, algorithm="cave")
```

Inside the engine, the decision is:

- use native C/C++ when available
- fallback to Python implementation when not available

This guarantees compatibility and easy deployment.

---

## 5. Recommended architecture

```text
+-----------------------------------------------------------+
|                    Python Application Layer                 |
|  Flask API / Streamlit / Web UI                           |
|  validates input, selects algorithm, formats response      |
+-----------------------------------------------------------+
                             |
                             v
+-----------------------------------------------------------+
|                 Compatibility Engine Wrapper                |
|  generate_map() / export_map() / bitmask_map()             |
|  chooses native implementation or Python fallback         |
+-----------------------------------------------------------+
                             |
               +-------------+---------------+
               v                             v
+---------------------+      +----------------------------+
| Python generator    |      | Native C/C++ module        |
| prototype_gen.py    |      | mapgen_core.dll /.so       |
| fallback logic      |      | heavy calculations         |
+---------------------+      +----------------------------+
```

This architecture allows the project to evolve without changing the frontend or API contracts.

---

## 6. Transition strategy by component

### 6.1 Cellular automata

This is an ideal first port because the algorithm is straightforward and data-local.

Current Python behavior:

- initialize grid randomly
- apply border walls
- iterate multiple smoothing passes
- use Moore neighborhood rules
- cleanup unreachable cavities

C/C++ conversion:

- allocate one flat buffer in memory
- iterate with pointer arithmetic
- compute neighbor counts in native code
- return compact grid data to Python

This keeps the same logic but removes Python loop overhead.

### 6.2 Bitmask autotiling

Bitmasking is also a good native candidate because it is a per-cell calculation with low branching complexity.

Python version:

- inspect neighbors N, E, S, W
- compute mask value 0..15
- map mask to tile image or sprite index

Native version:

- run full-grid mask pass in one contiguous pass
- store mask as integer data
- return mask matrix to Python for rendering

This is efficient and simple to keep compatible.

### 6.3 BFS flood fill

This algorithm is expensive in Python because of repeated object creation and hash/set operations.

Native version:

- use a queue array
- mark visited cells in a flat boolean buffer
- find the largest connected region
- fill isolated cavities

This preserves output semantics while drastically improving speed.

### 6.4 Noise generation

Perlin-like or smooth value noise is numeric-heavy and is a strong C/C++ candidate.

Native conversion:

- generate height values with interpolation and hashing
- compute multi-octave noise in one pass
- return grid values as float array

The Python layer can still interpret the resulting heightmap and map it into terrain categories.

---

## 7. How to keep compatibility with the existing project

### 7.1 Preserve the API contract

The Flask server routes should remain:

- POST /api/generate
- POST /api/export

The payload and output remain unchanged.

Python code should still serialize:

- map matrix as JSON
- PNG as bytes
- metadata like seed, dimensions, algorithm, and style

### 7.2 Keep the same output format

Even if generation now happens in native code, the result returned to the frontend should still be:

```json
{
  "grid": [[0, 1, 0], [1, 1, 0]],
  "seed": 42,
  "width": 3,
  "height": 2,
  "algorithm": "cave"
}
```

or a PNG export stream.

### 7.3 Preserve fallback logic

When the native plugin is missing or fails to load:

- automatically use Python generator
- print a warning
- maintain functionality

This gives a safe upgrade path for local development and deployment.

---

## 8. C/C++ integration choices

There are three practical options.

### Option A: C via ctypes

Best for a minimum-change migration.

Benefits:

- easy to integrate with existing Python project
- no complex build system required
- good for performance-critical loops

Use when:

- the project is still primarily Python-based
- the goal is speedup without large refactor

### Option B: C++ with pybind11

Best for a cleaner object-oriented integration model.

Benefits:

- better type safety
- easier to expose classes and functions
- better long-term maintainability

Use when:

- the project will grow into a larger engine
- multiple native modules are planned

### Option C: WebAssembly for browser-side execution

Best for frontend-only acceleration.

Benefits:

- extremely low latency in browser
- no server CPU cost for generation

Use when:

- the UI needs real-time map preview generation on the client side

For this project, Option A or Option B is the most practical choice.

---

## 9. Recommended migration sequence

### Phase 1: Isolate hot algorithms

Move these Python functions into a dedicated engine module:

- generate_cave_grid()
- smooth_cave_grid()
- flood_fill_cleanup()
- compute_bitmask_grid()
- generate_noise_heightmap()

At this stage, no public behavior changes.

### Phase 2: Introduce native wrapper

Create a compatibility layer that decides:

- Python implementation
- native C/C++ implementation

This should be done behind the same public method names.

### Phase 3: Validate determinism

Compare outputs for the same seed before and after porting.

Check:

- same dimensions
- same open/closed tiles
- same PNG export output
- same custom tile mapping behavior

### Phase 4: Integrate with backend API

Update the Flask backend so that the API still returns the same JSON or PNG results.

### Phase 5: Add performance benchmarking

Measure:

- generation time in Python
- generation time in C/C++
- memory usage
- export speed

This helps prove the benefit of the migration.

---

## 10. Project workflow: Case A and Case B

The application should operate through two user paths.

---

### Case A: User wants a level without custom assets

This is the fast path for non-technical users.

#### Flow

1. User opens the generator interface.
2. User selects a preset theme such as:
   - cave
   - dungeon
   - forest / terrain
3. The app loads the corresponding preset bitmask mapping automatically.
4. The user sets generation parameters, such as:
   - seed
   - width and height
   - algorithm type
   - number of smoothing passes
5. The backend generates the map using the selected engine.
6. The bitmask mapping is applied to the generated matrix.
7. The map is rendered on canvas.
8. The result is exported as PNG or JSON.

#### Characteristics

- no manual tile assignment needed
- faster workflow
- ideal for default level generation
- uses prebuilt sprite mapping and preset files

#### Project structure support

This can be handled by:

- backend/presets/
- preset JSON files mapping mask IDs to sprite positions
- automatic loading from the selected theme

---

### Case B: User uploads their own tile asset sheet

This is the custom asset path.

#### Flow

1. User chooses custom tilesheet mode.
2. User uploads a PNG or sprite sheet.
3. The system detects tile dimensions and shows the sheet in an editor.
4. The user assigns each of the 16 bitmask states to the corresponding tile region.
5. The interface asks the user to map values such as:
   - 0: isolated tile
   - 1: north connection
   - 2: east connection
   - 3: northeast corner
   - ...
   - 15: fully surrounded tile
6. The custom mapping is saved as JSON.
7. The generator runs and uses the custom mapping to render the final level.
8. The result can be exported as PNG or saved as a custom preset.

#### Characteristics

- user has control over art style and tile layout
- works for custom game themes
- requires bitmasking before map generation

#### Important rule

The custom bitmask mapping is not optional for the rendering step. If a mask is missing, the app should either:

- fallback to a default tile
- warn the user that some states are unassigned
- color the missing mask as a placeholder tile

This keeps the system robust.

---

## 11. Recommended project structure for this workflow

```text
Map Gen/
├── backend/
│   ├── algorithms/
│   │   ├── base.py
│   │   ├── prototype_gen.py
│   │   ├── c_bridge.py
│   │   └── native_engine.py
│   ├── export/
│   │   └── prototype_export.py
│   ├── presets/
│   │   ├── cave_preset.json
│   │   ├── dungeon_preset.json
│   │   └── overworld_preset.json
│   ├── native/
│   │   ├── mapgen_core.c
│   │   ├── mapgen_core.h
│   │   └── mapgen_core.dll / .so
│   └── app.py
│
├── frontend/
│   ├── app.py
│   ├── index.html
│   └── style.css
│
├── web/
│   ├── cellular.html
│   ├── bsp.html
│   ├── perlin.html
│   └── bitmask editor UI pages
│
├── documentation/
│   ├── README.md
│   ├── Transtition.md
│   └── project docs
│
├── tests/
│   └── test_prototype.py
└── requirements.txt
```

---

## 12. Best-practice implementation flow

The cleanest practical flow for the project is:

1. Keep the Python version as the reference implementation.
2. Identify expensive functions and isolate them.
3. Port one algorithm at a time to C/C++.
4. Add a native wrapper that preserves the same function names.
5. Keep Python fallback logic enabled.
6. Validate outputs against the Python version using seeds.
7. Integrate the native path into the backend API.
8. Support both preset assets and custom tile assets in the UI.
9. Save custom bitmask mappings as JSON presets for reuse.
10. Maintain a simple final rendering pipeline that accepts either default or custom tile mapping.

---

## 13. Final recommendation

The best approach for this project is not to rewrite everything in C/C++, but to gradually port only the computational hot spots while leaving the application design and user workflow intact.

This means:

- Python remains the orchestrator and project interface
- C/C++ handles performance-heavy matrix logic
- preset-based generation remains the default simple path
- custom tile sheets remain an advanced option requiring bitmask assignment
- the project remains compatible across backend, frontend, and export workflows

This gives the project a clear upgrade path from a Python-first prototype into a faster, production-friendly procedural generation engine without breaking the user experience.

---

## 14. Summary

The transition to C/C++ should be done as a compatibility-driven refactor, not a full rewrite. The project should keep its public API, output shape, and user flow stable while gradually moving heavy operations to native code.

The working model is:

- Case A: choose preset assets, generate level, render immediately
- Case B: upload tiles, bitmask them, generate custom styled level
- native C/C++: accelerate generation tasks while preserving Python orchestration

This gives the project both performance and long-term scalability.
