# ⚙️ Backend Module — MapGen API Engine

Welcome to the **Backend Engine** directory! This folder contains the server logic that receives user requests, generates procedural map grids, and exports map images.

---

## 🧒 Explain Like I'm 5 (ELI5)

> Think of the backend like a **toy kitchen order counter**:
>
> 1. You stand at the window (the **API Endpoint**) and ask: *"Can I have a cave map with seed number 42?"*
> 2. The order counter hands your request to the **Chef** (`MapGenApp`).
> 3. The Chef picks up a **Grid Recipe** (`PrototypeGridGenerator`) and makes a 20×20 matrix grid of 0s and 1s.
> 4. If you asked for a picture instead, the Chef hands the grid to the **Painter Robot** (`PNGExporter`), who draws a pretty PNG picture and hands it right back to you!

---

## ⚙️ How It Works & Methodology

The backend is engineered using **Object-Oriented Programming (OOP)** and clean architectural patterns:

- **Factory Pattern & Dependency Injection**:
  - `MapGenApp` encapsulates the Flask server lifecycle.
  - The map algorithm (`generator_class`) and exporter (`exporter`) are passed in as dependencies, making it super easy to swap algorithms or exporters without changing server routes!
- **Single Responsibility Principle (SRP)**:
  - Routing logic lives in [app.py](file:///e:/Projects/PBL/Map%20Gen/backend/app.py).
  - Procedural generation lives in [backend/algorithms/](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/README.md).
  - PNG rendering lives in [backend/export/](file:///e:/Projects/PBL/Map%20Gen/backend/export/README.md).

---

## 📂 Subdirectories & Files

| File / Folder | Purpose |
| :--- | :--- |
| 📄 [`app.py`](file:///e:/Projects/PBL/Map%20Gen/backend/app.py) | Main Flask server entry point. Configures CORS and handles API endpoints. |
| 📄 [`__init__.py`](file:///e:/Projects/PBL/Map%20Gen/backend/__init__.py) | Package initialization file for module importing. |
| 📂 [`algorithms/`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/README.md) | Contains procedural generation algorithms (Base generator & Cellular Automata). |
| 📂 [`export/`](file:///e:/Projects/PBL/Map%20Gen/backend/export/README.md) | Handles image rendering and PNG file generation. |

---

## 📡 REST API Endpoints

### 1. `GET /health`
- **Purpose**: Health check probe to ensure the server is active.
- **Response**: `{"status": "ok"}` (HTTP 200)

### 2. `POST /api/generate`
- **Purpose**: Generates a 2D integer grid (matrix) based on parameters.
- **Request Body**:
  ```json
  {
    "seed": 42,
    "width": 20,
    "height": 20
  }
  ```
- **Response Body**:
  ```json
  {
    "matrix": [[1, 1, 0, ...], ...],
    "seed": 42
  }
  ```

### 3. `POST /api/export`
- **Purpose**: Generates a 2D map and returns a downloadable high-res PNG image.
- **Response**: Binary PNG download file `mapgen_seed42_20x20.png`.

---

## 🎮 How to Run

Run the backend server directly from the root directory:
```bash
python backend/app.py
```
Or as a module:
```bash
python -m backend.app
```
Server runs at: `http://localhost:5000`
