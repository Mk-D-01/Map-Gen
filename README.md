# 🗺️ MapGen Engine — Procedural Map Generator

Welcome to **MapGen Engine**! A procedural grid map generation platform built with Python Streamlit and Python Flask. It generates caves, dungeons, and terrain maps using procedural algorithms including Cellular Automata, Perlin Noise, and Binary Space Partitioning.

---

## 🔬 System Architecture & How It Works

MapGen Engine is built around three core architectural layers:

```
+-------------------------------------------------------------------+
|               Streamlit Web Application (frontend/app.py)         |
|  - Interactive Controls & Multi-Tab Algorithmic Suite             |
|  - Dual Mode: Direct Engine Import & Flask REST API Mode          |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                     Python Flask REST API Server                  |
|  - MapGenApp Container & API Routes (backend/app.py)             |
|  - Cellular Automata Engine (backend/algorithms/prototype_gen.py) |
|  - In-Memory Pillow PNG Streamer (backend/export/prototype_export)|
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                     Pytest Automated Test Harness                 |
|  - Seed Determinism & Matrix Validation (tests/test_prototype.py) |
+-------------------------------------------------------------------+
```

1. **Python Flask Backend (`/backend`)**:
   - Implements Object-Oriented design patterns (Factory Pattern, Strategy Pattern, Abstract Base Classes).
   - Exposes REST API endpoints (`/api/generate` and `/api/export`).
   - Uses Pillow (PIL) and `io.BytesIO` to stream PNG image downloads directly in memory without writing temporary files to disk.
2. **Streamlit Interactive Frontend (`/frontend/app.py`)**:
   - Python Streamlit application suite featuring interactive parameter sliders, cellular automata step-by-step visualizer, procedural noise suite, and spatial hashing analysis.
   - Operates in both Direct Python Engine mode (in-memory execution) and REST API mode.
3. **Automated Test Suite (`/tests`)**:
   - Pytest unit and integration test suite asserting pseudo-random number generator (PRNG) seed determinism, matrix bounds, and PNG magic byte headers.

---

## 👥 Directory Structure & Role Ownership Matrix

Each module in the repository is maintained by a dedicated engineering role guide:

| Directory | Module Description | Owning Role Guide | Primary Technical Focus |
| :--- | :--- | :--- | :--- |
| ⚙️ [`backend/`](file:///e:/Projects/PBL/Map%20Gen/backend/BACKEND_ENGINEER_ROLE.md) | Flask REST API & Engine | [Backend Engineer Guide](file:///e:/Projects/PBL/Map%20Gen/backend/BACKEND_ENGINEER_ROLE.md) | REST APIs, WSGI routing, CORS, OOP architecture |
| 🧠 [`backend/algorithms/`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/ALGORITHM_DESIGNER_ROLE.md) | Procedural Algorithms | [Algorithm Designer Guide](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/ALGORITHM_DESIGNER_ROLE.md) | Cellular Automata, Moore Neighborhood, Seed determinism |
| 🎨 [`backend/export/`](file:///e:/Projects/PBL/Map%20Gen/backend/export/EXPORTER_ENGINEER_ROLE.md) | Graphics & PNG Exporter | [Graphics Exporter Guide](file:///e:/Projects/PBL/Map%20Gen/backend/export/EXPORTER_ENGINEER_ROLE.md) | Pillow rasterization, `BytesIO` streaming, RGB palette |
| 🎨 [`frontend/`](file:///e:/Projects/PBL/Map%20Gen/frontend/FRONTEND_ENGINEER_ROLE.md) | Streamlit Client Web Suite | [Frontend Engineer Guide](file:///e:/Projects/PBL/Map%20Gen/frontend/FRONTEND_ENGINEER_ROLE.md) | Streamlit widgets, state management, matrix rendering |
| 🌐 [`web/`](file:///e:/Projects/PBL/Map%20Gen/web/WEB_VISUALIZER_ROLE.md) | Visualizer Suite | [Web Visualizer Guide](file:///e:/Projects/PBL/Map%20Gen/web/WEB_VISUALIZER_ROLE.md) | Perlin Noise, BSP Tree, Spatial Hashing $O(1)$ lookup |
| 🧪 [`tests/`](file:///e:/Projects/PBL/Map%20Gen/tests/TEST_ENGINEER_ROLE.md) | Automated Test Suite | [Test Engineer Guide](file:///e:/Projects/PBL/Map%20Gen/tests/TEST_ENGINEER_ROLE.md) | Pytest fixtures, seed reproducibility, image assertions |
| 📚 [`documentation/`](file:///e:/Projects/PBL/Map%20Gen/documentation/TECHNICAL_WRITER_ROLE.md) | System Documentation | [Technical Writer Guide](file:///e:/Projects/PBL/Map%20Gen/documentation/TECHNICAL_WRITER_ROLE.md) | Setup guides, installation manuals, API documentation |
| 🎓 [`collageRequirement/`](file:///e:/Projects/PBL/Map%20Gen/collageRequirement/ACADEMIC_LEAD_ROLE.md) | Academic Specifications | [Academic Lead Guide](file:///e:/Projects/PBL/Map%20Gen/collageRequirement/ACADEMIC_LEAD_ROLE.md) | PBL project proposal, academic requirements |
| 🏛️ [`previousStack/`](file:///e:/Projects/PBL/Map%20Gen/previousStack/LEGACY_C_ENGINEER_ROLE.md) | Legacy C Prototypes | [Legacy C Engineer Guide](file:///e:/Projects/PBL/Map%20Gen/previousStack/LEGACY_C_ENGINEER_ROLE.md) | C source code, compiled binaries, performance proof |
| 🖼️ [`assets/`](file:///e:/Projects/PBL/Map%20Gen/assets/GRAPHICS_DESIGNER_ROLE.md) | Visual Resources | [Graphics Designer Guide](file:///e:/Projects/PBL/Map%20Gen/assets/GRAPHICS_DESIGNER_ROLE.md) | Tile sets, sprite packs, UI screenshots |
| 👑 [`roles/`](file:///e:/Projects/PBL/Map%20Gen/roles/README.md) | Team Roles Hub | [Overviewer Guide](file:///e:/Projects/PBL/Map%20Gen/roles/OVERVIEWER_ROLE.md) | Team role guidelines & responsibility matrix |

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.9+ installed

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch Streamlit Web Application
```bash
streamlit run frontend/app.py
```

### 3. (Optional) Run Flask Backend REST API
```bash
python backend/app.py
```

---

## 🛠 Running Automated Tests
Run the Pytest suite from the root folder:
```bash
pytest tests/
```
