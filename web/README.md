# 🌐 Web Module — Interactive Visualizer Suite

Welcome to the **Web Module**! This directory contains a standalone, browser-executable visualizer suite showcasing multiple procedural map generation algorithms and spatial data structures.

---

## 🧒 Explain Like I'm 5 (ELI5)

> Imagine a **Magic Map Museum** where each room has a different toy robot showing off a cool trick:
>
> 1. **Cellular Automata Room** (`cellular.html`): Shows how random dots smooth themselves out into cave tunnels!
> 2. **Perlin Noise Room** (`perlin.html`): Shows how smooth waves make mountains, grass, and ocean water!
> 3. **BSP Room** (`bsp.html` & `bsp-tree.html`): Slices a large piece of paper in half over and over to make rooms and corridors like a castle!
> 4. **Spatial Hash & Grid Rooms** (`spatial-hash.html`, `spatial-grid.html`): Shows how a smart radar sorts toys into grid boxes so it can find things instantly!

---

## ⚙️ How It Works & Methodology

The Web Visualizer Suite runs purely on client-side JavaScript without requiring any backend installation:

- **Procedural Generation Demos**:
  - **Cellular Automata**: Live step-by-step animation of cave smoothing passes.
  - **Perlin Noise**: 2D smooth gradient noise generation for terrain heightmaps (ocean, sand, grass, mountain, snow).
  - **Binary Space Partitioning (BSP)**: Recursive space splitting tree algorithm for dungeon generation with room connections.
  - **Moore Neighbourhood**: Interactive visualization of 8-neighbor cell inspection.
- **Spatial Partitioning & Optimization**:
  - **Spatial Hash & Spatial Grid**: Demonstrates fast collision detection and neighbor queries ($O(1)$ lookup complexity instead of $O(N^2)$ brute force).

---

## 📂 Visualizer Suite Pages

| Page | Algorithm / Concept | Description |
| :--- | :--- | :--- |
| 📄 [`index.html`](file:///e:/Projects/PBL/Map%20Gen/web/index.html) | Hub Overview | Main dashboard linking to all visualizers and algorithm interactive demos. |
| 📄 [`cellular.html`](file:///e:/Projects/PBL/Map%20Gen/web/cellular.html) | Cellular Automata | Interactive cave visualizer with live slider controls for smooth passes and wall fill density. |
| 📄 [`perlin.html`](file:///e:/Projects/PBL/Map%20Gen/web/perlin.html) | Perlin Noise | Terrain heightmap generator with color-coded elevation layers. |
| 📄 [`bsp.html`](file:///e:/Projects/PBL/Map%20Gen/web/bsp.html) | BSP Dungeon | Room & corridor generator using Binary Space Partitioning. |
| 📄 [`bsp-tree.html`](file:///e:/Projects/PBL/Map%20Gen/web/bsp-tree.html) | BSP Tree Visualizer | Node hierarchy tree graph visualization of spatial partitioning splits. |
| 📄 [`moore-neighborhood.html`](file:///e:/Projects/PBL/Map%20Gen/web/moore-neighborhood.html) | Moore Neighborhood | 8-cell direction matrix visualizer ($N, NE, E, SE, S, SW, W, NW$). |
| 📄 [`spatial-grid.html`](file:///e:/Projects/PBL/Map%20Gen/web/spatial-grid.html) | Spatial Grid | 2D uniform grid partitioning demo. |
| 📄 [`spatial-hash.html`](file:///e:/Projects/PBL/Map%20Gen/web/spatial-hash.html) | Spatial Hashing | Constant-time spatial bucket hashing for dynamic entities. |
| 📄 [`app.js`](file:///e:/Projects/PBL/Map%20Gen/web/app.js) | JS Engine | Core standalone algorithms and visualizer rendering logic. |
| 📄 [`styles.css`](file:///e:/Projects/PBL/Map%20Gen/web/styles.css) | Master Styling | Design system CSS for dark themes, interactive controls, and canvas cards. |

---

## 🎮 How to Run

Simply open [`web/index.html`](file:///e:/Projects/PBL/Map%20Gen/web/index.html) in your favorite web browser! No server setup required.
