# 🖼️ Graphics Designer Role Guide — Visual Resources & Tile Packs

**Role**: UI/UX & Tile Assets Designer  
**Scope**: Graphic Tile Sets, Sprite Packs, Map Screenshots, UI Preview Assets  
**Primary Directory**: [`assets/`](file:///e:/Projects/PBL/Map%20Gen/assets/GRAPHICS_DESIGNER_ROLE.md)

---

## 🔬 How It Works Under the Hood

The assets module stores graphical resources, terrain textures, tile sprite packs, and preview captures used across the web applications and documentation.

```
                           +------------------------------------------+
                           |   assets/GRAPHICS_DESIGNER_ROLE.md       |
                           +------------------------------------------+
                                                |
              +---------------------------------+---------------------------------+
              v                                                                   v
+------------------------------------------+                       +------------------------------------------+
| Terrain Tile Sets                        |                       | UI & Preview Captures                    |
| - Ground textures, rock walls, paths     |                       | - Map export samples                     |
| - Numerical asset packs (1/, 2/, 3/)     |                       | - Documentation screenshots (Pack 5/)    |
+------------------------------------------+                       +------------------------------------------+
```

### 1. Tile Pack Subdirectories
- **`1/`**: Primary terrain sprite tilesets used for ground, path, and wall visualizers.
- **`2/`**: Secondary terrain height textures for biome rendering.
- **`3/`**: Canvas UI graphic assets and icon elements.
- **`5/`**: Benchmark map captures and export previews.

---

## 📂 Subsystem Directory Overview

| Directory | Purpose |
| :--- | :--- |
| 📂 `1/` | Primary tile set & map preview assets (Pack 1). |
| 📂 `2/` | Secondary visual assets & terrain textures (Pack 2). |
| 📂 `3/` | Additional UI & canvas preview assets (Pack 3). |
| 📂 `5/` | Sample output renders and exported map benchmarks (Pack 5). |
