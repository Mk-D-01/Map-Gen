# 🌐 Interactive Visualizer Role Guide — Standalone Algorithmic Suite

**Role**: Interactive Visualizer Engineer  
**Scope**: Standalone JS Algorithms, Perlin Noise Terrain, Binary Space Partitioning (BSP), Spatial Hashing  
**Primary Directory**: [`web/`](file:///e:/Projects/PBL/Map%20Gen/web/WEB_VISUALIZER_ROLE.md)

---

## 🔬 How It Works Under the Hood

The Web Visualizer Suite is a client-side showcase of procedural generation algorithms and spatial optimization data structures. It runs purely in the browser without requiring a backend server.

```
                      +----------------------------------+
                      |       web/index.html Hub         |
                      +----------------------------------+
                                       |
       +------------------+------------+------------+------------------+
       |                  |                         |                  |
       v                  v                         v                  v
+--------------+   +--------------+          +--------------+   +--------------+
| Cellular     |   | Perlin Noise |          | BSP Dungeon  |   | Spatial Hash |
| Automata     |   | Heightmap    |          | Room Splits  |   | Bucket Lookup|
+--------------+   +--------------+          +--------------+   +--------------+
```

### 1. Perlin 2D Terrain Heightmaps (`perlin.html`)
- Calculates smooth 2D gradient noise to generate continuous terrain heightmaps.
- Color-codes elevation layers into biomes: Ocean, Sand, Grass, Mountain, and Snow.

### 2. Binary Space Partitioning Dungeon Generator (`bsp.html`, `bsp-tree.html`)
- Recursively divides a grid area into smaller rectangular rooms using a BSP tree structure.
- Connects sibling room centroids using L-shaped corridor paths.
- Provides a live tree graph visualizer (`bsp-tree.html`) showing node splitting hierarchies.

### 3. Spatial Hashing & Fast Lookup (`spatial-hash.html`, `spatial-grid.html`)
- Assigns 2D positions to spatial grid buckets using a hash formula.
- Reduces collision and neighbor lookup operations from slow $O(N^2)$ brute-force down to fast $O(1)$ constant time lookup.

---

## 📂 Visualizer Suite Pages

| Page | Algorithm / Concept | Purpose |
| :--- | :--- | :--- |
| 📄 [`index.html`](file:///e:/Projects/PBL/Map%20Gen/web/index.html) | Visualizer Dashboard | Main overview hub linking to all visualizers. |
| 📄 [`cellular.html`](file:///e:/Projects/PBL/Map%20Gen/web/cellular.html) | Cellular Automata | Interactive cave visualizer with live slider controls and animated smoothing passes. |
| 📄 [`perlin.html`](file:///e:/Projects/PBL/Map%20Gen/web/perlin.html) | Perlin Noise | Terrain heightmap generator with color-coded elevation layers. |
| 📄 [`bsp.html`](file:///e:/Projects/PBL/Map%20Gen/web/bsp.html) | BSP Dungeon | Room and corridor generator using Binary Space Partitioning. |
| 📄 [`bsp-tree.html`](file:///e:/Projects/PBL/Map%20Gen/web/bsp-tree.html) | BSP Tree Visualizer | Node hierarchy tree graph visualization showing space splits. |
| 📄 [`moore-neighborhood.html`](file:///e:/Projects/PBL/Map%20Gen/web/moore-neighborhood.html) | Moore Neighborhood | Interactive 8-neighbor cell direction matrix demo. |
| 📄 [`spatial-grid.html`](file:///e:/Projects/PBL/Map%20Gen/web/spatial-grid.html) | Spatial Grid | 2D uniform grid partitioning demo. |
| 📄 [`spatial-hash.html`](file:///e:/Projects/PBL/Map%20Gen/web/spatial-hash.html) | Spatial Hashing | Fast spatial bucket lookup demo. |
| 📄 [`app.js`](file:///e:/Projects/PBL/Map%20Gen/web/app.js) | Standalone JS Engine | Pure JavaScript implementations of all algorithms and visualizer loops. |
| 📄 [`styles.css`](file:///e:/Projects/PBL/Map%20Gen/web/styles.css) | Visualizer Styling | Master CSS stylesheet for dark themes, canvas cards, and control panels. |

---

## 🎮 Execution Instructions

Open [`web/index.html`](file:///e:/Projects/PBL/Map%20Gen/web/index.html) directly in any modern web browser. No server setup required.
