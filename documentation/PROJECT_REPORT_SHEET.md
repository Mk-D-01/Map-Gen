# 🗺️ MapGen Engine — Product Feature Report Sheet

**Document Purpose**: Product Capability & Roadmap Specification  
**Project**: MapGen Engine (Procedural Content Generation Platform)  
**Focus**: **What the product DOES** (User Capabilities & Deliverables) and **Future Iterations**  
**Document Version**: 1.1.0  
**Current Milestone**: Phase 1 Shipped (Operational Prototype)  

---

## 📌 Executive Summary

**MapGen Engine** is an automated level design and procedural environment generation platform. It eliminates the time-consuming process of manually drawing 2D game maps, dungeon levels, and cavern systems. By giving creators a simple interface to input a numeric seed or randomize parameters, MapGen Engine synthesizes structured, coherent, and ready-to-use 2D game worlds in milliseconds.

Rather than describing internal code mechanics, this report sheet provides a comprehensive overview of **what capabilities the product delivers to users today**, and **what new functionalities will arrive in future product iterations**.

---

## 🚀 Features Currently Shipped (What the Product Does)

The table below outlines the end-user capabilities currently available in the shipped product:

| # | Shipped Feature | What It Does (User-Facing Capability) | Delivery Format |
| :-: | :--- | :--- | :--- |
| **1** | **One-Click Cave & Maze Generation** | Generates natural-looking 2D cavern networks, tunnels, and maze environments instantly without manual level drafting. | Interactive Browser Canvas & Data Matrix |
| **2** | **Deterministic World Seeding** | Creates exact, reproducible worlds. Entering the same seed number produces the exact same map layout every time, allowing level sharing between players. | Seed Input Field (e.g., `42`) |
| **3** | **Custom Dimension Sizing** | Allows designers to choose their desired grid size, from compact $5 \times 5$ tactical rooms up to massive $100 \times 100$ exploration maps. | Width & Height Selectors |
| **4** | **Real-Time Interactive Canvas** | Renders the generated world live in the browser with responsive scaling, crisp pixel rendering, and dark-mode visual styling. | HTML5 Canvas Viewport |
| **5** | **Instant Game-Ready PNG Export** | Downloads the generated map as a clean, high-resolution PNG image with a single click, ready to drop into Unity, Godot, or Unreal. | One-Click `.png` Download |
| **6** | **Live Generation Metrics** | Informs designers of the exact map dimensions, active floor area, and wall density percentages immediately after generation. | Dynamic Metadata Bar |
| **7** | **Headless Game Integration API** | Provides an HTTP service that external games, standalone apps, or Discord bots can query to receive new maps or images programmatically. | REST Endpoints (`/api/generate`, `/api/export`) |
| **8** | **Multi-Algorithm Exploration Lab** | Provides interactive web showcases where creators can test and compare different terrain styles (Perlin biomes, BSP dungeons, and Cellular caves). | Multi-Page Algorithmic Suite (`/web`) |
| **9** | **Built-in Quality Safeguards** | Protects users from invalid entries (e.g., negative dimensions or empty seeds) by automatically enforcing safe bounds and returning clear error messages. | Form Validation & HTTP Status Codes |

---

### Detailed Feature Breakdown

### 1. Instant Cavern & Level Synthesis
- **What it does**: Turns an empty canvas into an organic, playable cavern system featuring cavern chambers, winding passages, and protective perimeter walls.
- **Value to creators**: Eliminates "blank canvas paralysis." Game designers can create hundreds of distinct level layouts in seconds during game jams or rapid prototyping.

### 2. Shareable & Reproducible World Seeds
- **What it does**: Ties every layout to a specific number or phrase. If a player finds an exciting layout under seed `9482`, any other user on any device who enters `9482` gets that exact same level.
- **Value to creators**: Powers daily challenge modes, multiplayer world synchronization, and reproducible bug testing for game studios.

### 3. Dynamic Map Sizing
- **What it does**: Gives designers full control over the width and height of the playing field. Whether making a single-screen retro puzzle game ($20 \times 20$) or a large dungeon crawler ($100 \times 100$), the generator adjusts seamlessly.
- **Value to creators**: Fits any screen resolution, aspect ratio, or gameplay scope.

### 4. Interactive Visualizer Viewport
- **What it does**: Displays the generated map immediately on screen with crisp, high-contrast colors (e.g., dark charcoal walls and warm illuminated floor pathways) and automatic layout centering.
- **Value to creators**: Allows creators to evaluate room density, chokepoints, and flow visually before saving or exporting.

### 5. Direct PNG Asset Download
- **What it does**: Converts the generated spatial map directly into a downloaded PNG image file with correct headers and clean pixel lines.
- **Value to creators**: Assets can be immediately imported into tools like Photoshop, Aseprite, Tiled, or dragged directly into game engine sprite assets.

### 6. Headless HTTP API Service
- **What it does**: Runs as a background service with dedicated web endpoints (`/api/generate` and `/api/export`). External applications can send a request with a seed and receive either raw matrix data or rendered image bytes.
- **Value to creators**: Allows games to generate new levels dynamically while the game is running—such as generating a new cave floor when a player steps onto a staircase.

### 7. Interactive Algorithm Sandbox Suite
- **What it does**: Gives users dedicated interactive pages to visualize different environment styles:
  - **Caves & Tunnels**: Cellular Automata organic smoothing.
  - **Hills & Biomes**: Perlin smooth noise terrain elevation.
  - **Dungeon Rooms & Corridors**: Binary Space Partitioning (BSP) structured room splits.
- **Value to creators**: Helps developers choose the ideal environmental style for their specific game genre.

---

## 🔮 Future Iterations & Roadmap (What Upcoming Versions Will Do)

The MapGen Engine product roadmap expands from standalone generation into a full-featured level authoring suite. Here is what future iterations will deliver:

```
+---------------------------------------------------------------------------------------------+
|                                  PRODUCT EVOLUTION ROADMAP                                  |
|                                                                                             |
|   [ SHIPPED ]        [ ITERATION 2 ]        [ ITERATION 3 ]        [ ITERATION 4 ]          |
|  Phase 1 Baseline  -> Smart Tunnels &   -> Dynamic Tile Themes  -> Universal Game Engine    |
|  Seed, Canvas,        Guaranteed Paths     & Creature Spawns       Exporters & Playtester   |
|  PNG Export & API     (No Dead Ends)       (Pixel Art Assets)      (Direct Tiled / Godot)   |
+---------------------------------------------------------------------------------------------+
```

---

### 🌟 Iteration 2: Smart Tunnels & Guaranteed Connectivity
*Target: Q3 2026*

- **Guaranteed Traversability**:
  - **What it will do**: Analyzes the generated map to ensure that there are no isolated, inaccessible pockets. Every open cavern and room will have a confirmed walkable path connecting to the rest of the map.
  - **Auto-Carving Passages**: Automatically cuts clean connection corridors between disconnected rooms so players never get stuck behind impenetrable walls.
- **Customizable Room Density Sliders**:
  - **What it will do**: Gives users intuitive sliders for "Roughness", "Openness", and "Corridor Tightness", allowing one-click switching between tight labyrinth mazes and expansive open caverns.

---

### 🌟 Iteration 3: Visual Theme Packs & Autotiling (Pixel Art Worlds)
*Target: Q4 2026*

- **Smart Autotiling**:
  - **What it will do**: Replaces basic solid color squares with detailed sprite graphics that automatically blend. Walls will have textured stone tops, corner shadows, and border edges that wrap around floor tiles seamlessly.
- **Multi-Environment Theme Switcher**:
  - **What it will do**: Allows users to switch the visual skin of their map with a single click between:
    - *Underground Obsidian Dungeon*
    - *Lush Overworld Forest & Rivers*
    - *Ancient Desert Ruins*
    - *Sci-Fi Space Station Corridors*
- **Elevation & Water Biomes**:
  - **What it will do**: Adds depth layers—water pools, shallow shallows, walkable ground, and elevated cliffs—creating multi-tier vertical gameplay.

---

### 🌟 Iteration 4: Gameplay Object, Enemy & Loot Placement
*Target: Early 2027*

- **Spawn & Objective Positioning**:
  - **What it will do**: Automatically places key gameplay elements:
    - Safe player starting zone.
    - Level exit portal / staircase.
    - Treasure chests placed inside hidden nooks and side caverns.
    - Boss arenas designated in the largest open chambers.
- **Difficulty & Encounter Pacing**:
  - **What it will do**: Allows creators to select a difficulty level (Casual, Normal, Hardcore) to adjust enemy spawn density and trap frequencies across the map.

---

### 🌟 Iteration 5: In-Browser Playable Character Walkthrough
*Target: Mid 2027*

- **Instant "Playtest" Mode**:
  - **What it will do**: Adds a "Play Map" button directly on the canvas. Designers can immediately control an on-screen character using WASD or arrow keys.
- **Line-of-Sight & Fog of War Preview**:
  - **What it will do**: Simulates dynamic player lighting and torch visibility, allowing creators to experience how tense or exploratory the map feels before exporting it.

---

### 🌟 Iteration 6: Universal Game Engine Export Suite
*Target: Late 2027*

- **Direct Tiled Editor Integration (`.tmx` / `.json`)**:
  - **What it will do**: Exports maps directly into the standard Tiled map editor format with pre-configured collision and background layers.
- **Godot 4.x & Unity 2D Native Support**:
  - **What it will do**: Generates ready-to-import TileMap data structures for Godot (`.tres` / `.tscn`) and Unity Tilemap arrays, enabling drag-and-drop game prototyping in seconds.
- **Vector Graphics (SVG) Export**:
  - **What it will do**: Generates infinite-resolution SVG vector maps suitable for high-resolution printing, posters, or tabletop campaign handouts (D&D / TTRPGs).

---

### 🌟 Iteration 7: Cloud Preset Library & Community Hub
*Target: Future Expansion*

- **Online Seed Sharing Gallery**:
  - **What it will do**: A community gallery where creators can publish their coolest map designs, browse trending community seeds, and upvote favorite layouts.
- **One-Click Seed Bookmarking**:
  - **What it will do**: Lets users save personal favorite seeds with custom tags (e.g., *"Big Boss Arena"*, *"Tight Maze"*, *"Speedrun Friendly"*).

---

## 📊 Feature Comparison & Delivery Status Matrix

| Capability Category | Specific Feature | Shipped in Current Release | Arriving in Next Iteration | Future Roadmap |
| :--- | :--- | :---: | :---: | :---: |
| **Level Generation** | Organic 2D Cave Synthesis | ✅ **Shipped** | — | — |
| | Reproducible Numeric Seeds | ✅ **Shipped** | — | — |
| | Guaranteed Connected Rooms | ❌ | 🚀 **Iteration 2** | — |
| | Biome Elevation Layers (Multi-tier) | ❌ | — | 🚀 **Iteration 3** |
| **User Interface** | Real-Time Canvas Preview | ✅ **Shipped** | — | — |
| | Custom Grid Dimension Controls | ✅ **Shipped** | — | — |
| | Canvas Zoom & Pan Navigation | ❌ | 🚀 **Iteration 2** | — |
| | In-Browser Walkable Character | ❌ | — | 🚀 **Iteration 5** |
| **Visual Aesthetics** | Pixel-Crisp High-Contrast Grid | ✅ **Shipped** | — | — |
| | Autotiling Wall-Border Sprites | ❌ | — | 🚀 **Iteration 3** |
| | Multi-Theme Skins (Dungeon/Forest) | ❌ | — | 🚀 **Iteration 3** |
| **Export & Sharing** | PNG Image Download | ✅ **Shipped** | — | — |
| | Raw JSON Matrix Output | ✅ **Shipped** | — | — |
| | Tiled Editor (`.tmx` / `.json`) | ❌ | — | 🚀 **Iteration 6** |
| | Godot / Unity Native Presets | ❌ | — | 🚀 **Iteration 6** |
| | Cloud Seed Library & Community Hub | ❌ | — | 🚀 **Iteration 7** |
| **Gameplay Systems** | Spawn, Exit & Chest Placement | ❌ | — | 🚀 **Iteration 4** |
| | Difficulty & Trap Balancing | ❌ | — | 🚀 **Iteration 4** |

---

## 🎯 Target User Personas & Value Proposition

- **Indie Game Developers & Jam Teams**:  
  *Value*: Saves days of manual tile placement. Enables developers to build complete playable roguelike or dungeon-crawler prototypes in a single weekend.
- **Tabletop Game Masters (D&D / TTRPGs)**:  
  *Value*: Instantly generates battle maps and dungeon layouts with a single seed, printable as high-res graphics for in-person or virtual tabletop (VTT) sessions.
- **Game Design Students & Researchers**:  
  *Value*: Provides an interactive visual platform to observe how seed variables alter spatial flow, connectivity, and room structures.

---

## 📋 Document Information & Sign-Off

- **Maintained By**: Technical Documentation Team ([`documentation/`](file:///e:/Projects/PBL/Map%20Gen/documentation/README.md))
- **Related Project Guides**:
  - [Setup Guide](file:///e:/Projects/PBL/Map%20Gen/documentation/SETUP_GUIDE.md)
  - [Academic Milestone Report](file:///e:/Projects/PBL/Map%20Gen/collageRequirement/PROJECT_REPORT_SHEET.md)
  - [Roles Hub](file:///e:/Projects/PBL/Map%20Gen/roles/README.md)
- **Status**: Officially Released for Phase 1 Milestone Evaluation
