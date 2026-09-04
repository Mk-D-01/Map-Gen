# 🎨 Frontend Engineer Role Guide — Streamlit Web Application

**Role**: Frontend Web Engineer  
**Scope**: Streamlit Interface, PIL Raster Grid Mapping, Dual Engine Integration, Streamlit Downloads  
**Primary Directory**: [`frontend/`](file:///e:/Projects/PBL/Map%20Gen/frontend/FRONTEND_ENGINEER_ROLE.md)

---

## 🔬 How It Works Under the Hood

The frontend is built using **Python Streamlit** with custom dark glassmorphism styling. It supports dual execution modes: calling backend Python algorithms directly in-memory or communicating asynchronously with the Flask REST API.

```
 User Inputs                 Streamlit App (app.py)               Render Target
+--------------+            +-----------------------+            +----------------+
| Seed: 42     | ---------> | Direct Python Import  | ---------> | PIL RGB Image  |
| Width/Height |            | OR Flask REST API Call|            | Scaled Grid    |
+--------------+            +-----------------------+            +----------------+
                                       |
                                       v
                            +-----------------------+
                            | st.download_button()  | ---------> Download PNG / JSON
                            +-----------------------+
```

### 1. Streamlit Application Suite (`frontend/app.py`)
- Located in [`frontend/app.py`](file:///e:/Projects/PBL/Map%20Gen/frontend/app.py).
- **User Parameters**: Sidebar controls for grid width, grid height, wall fill probability, smoothing pass count, and RNG seed.
- **Dual Execution Modes**:
  - **⚡ Direct Python Engine**: Directly imports `PrototypeGridGenerator` from `backend.algorithms.prototype_gen` for high performance.
  - **🌐 Flask REST API**: Sends HTTP POST requests to `http://127.0.0.1:5000/api/generate`.

### 2. Matrix Image Rasterization
1. Receives the 2-D matrix array (0 = Floor, 1 = Wall).
2. Maps grid cells into a PIL RGB pixel matrix (`(30, 30, 46)` for walls, `(137, 180, 250)` for floors).
3. Upscales the image using Nearest-Neighbor interpolation (`Image.NEAREST`) to ensure crisp tile boundaries.

### 3. Native File Exporters
- Leverages Streamlit's `st.download_button()` paired with `backend/export/prototype_export.py` to stream PNG byte arrays (`image/png`) and JSON matrices directly to the user.

---

## 📂 Subsystem File Overview

| File | Purpose |
| :--- | :--- |
| 📄 [`app.py`](file:///e:/Projects/PBL/Map%20Gen/frontend/app.py) | Main Streamlit web application featuring controls, multi-tab visualizers, and PNG export handlers. |

---

## 🎮 How to Run

```bash
streamlit run frontend/app.py
```

