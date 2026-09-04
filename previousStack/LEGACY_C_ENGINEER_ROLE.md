# 🏛️ Legacy C Engineer Role Guide — Native Prototypes

**Role**: Low-Level Systems C Developer  
**Scope**: Legacy C Prototypes, Executable Binaries, Native Performance Benchmarking  
**Primary Directory**: [`previousStack/`](file:///e:/Projects/PBL/Map%20Gen/previousStack/LEGACY_C_ENGINEER_ROLE.md)

---

## 🔬 How It Works Under the Hood

The previous stack module contains early C-language prototypes and compiled executables. These served as proof-of-concept experiments before migrating to the modern Python Flask and JavaScript web stack.

```
                           +------------------------------------------+
                           |  previousStack/LEGACY_C_ENGINEER_ROLE.md |
                           +------------------------------------------+
                                                |
              +---------------------------------+---------------------------------+
              v                                                                   v
+------------------------------------------+                       +------------------------------------------+
| C Source Prototypes                      |                       | Compiled Binaries & Image Renders        |
| - map_gen_1.c (Matrix array logic)       |                       | - map_gen.exe / a.exe (Windows binaries) |
| - map_gen_image.c (PPM/PNG export logic) |                       | - map_output.png (Benchmark image)       |
+------------------------------------------+                       +------------------------------------------+
```

### 1. C-Language Algorithmic Proof of Concept
- **`map_gen_1.c`**: Implemented baseline random grid allocation, 2D array manipulation, and initial cellular smoothing logic written in raw C for maximum speed.
- **`map_gen_image.c`**: Added low-level file I/O byte manipulation to output raw image buffers directly to disk.

### 2. Native Benchmarks & Migration Path
- Proved that procedural cave generation could run in milliseconds.
- Provided the architectural blueprint for the current Python OOP backend (`backend/`) and client HTML5 Canvas engine (`frontend/`).

---

## 📂 Subsystem File Overview

| File | Type | Purpose |
| :--- | :--- | :--- |
| 📄 `map_gen_1.c` | C Source File | Baseline procedural map generator prototype written in C. |
| 📄 `map_gen_image.c` | C Source File | Extended C prototype with raw image output buffer creation. |
| 📄 `map_gen.exe` / `a.exe` | Executable | Compiled Windows binaries of the C map engine. |
| 🖼️ `map_output.png` | PNG Image | Sample map image render produced by the legacy C prototype. |
