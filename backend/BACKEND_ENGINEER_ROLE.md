# ⚙️ Backend Engineer Role Guide — MapGen API Engine

**Role**: Backend Software Engineer  
**Scope**: REST API Architecture, Server Lifecycle, OOP Engine Integration, Image Streaming  
**Primary Directory**: [`backend/`](file:///e:/Projects/PBL/Map%20Gen/backend/BACKEND_ENGINEER_ROLE.md)

---

## 🔬 How It Works Under the Hood

The backend subsystem is built with Python and Flask. It serves REST API endpoints that generate procedural grid matrices and render downloadable map images.

```
 Client Request                     Backend Server                     Engine Output
+--------------+               +----------------------+               +---------------+
| POST Request | ------------> |  MapGenApp (app.py)  | ------------> | 2D JSON Grid  |
| (Seed/Size)  |               |  - Validates Input   |               | or PNG Image  |
+--------------+               +----------------------+               +---------------+
                                          |
                        +-----------------+-----------------+
                        v                                   v
             +--------------------+              +--------------------+
             | PrototypeGridGen   |              | PNGExporter        |
             | (Generates Matrix) |              | (Renders Image)    |
             +--------------------+              +--------------------+
```

### 1. Server Structure & Routing
- The server entry point [`backend/app.py`](file:///e:/Projects/PBL/Map%20Gen/backend/app.py) encapsulates Flask routes inside the `MapGenApp` class.
- Cross-Origin Resource Sharing (CORS) is enabled so frontend clients can send API requests smoothly.

### 2. Map Generation Flow (`POST /api/generate`)
1. Client sends a JSON payload with `seed`, `width`, and `height`.
2. The server instantiates `PrototypeGridGenerator` with these parameters.
3. The algorithm builds a 2D matrix (a list of rows containing `0`s for paths and `1`s for walls).
4. The server responds with JSON containing the matrix data and the seed.

### 3. Direct Image Export Flow (`POST /api/export`)
1. Client sends map parameters to the export route.
2. The server generates the map matrix using `PrototypeGridGenerator`.
3. The matrix is handed to `PNGExporter`, which paints wall tiles and floor tiles using the Pillow image library.
4. Instead of writing files to disk, the PNG image is rendered directly into memory using `io.BytesIO` and streamed straight to the client browser as a file download.

---

## 📡 REST API Endpoints

| Endpoint | Method | Purpose | Sample Request Payload | Sample Response |
| :--- | :--- | :--- | :--- | :--- |
| `/health` | `GET` | Server health check probe | *None* | `{"status": "ok"}` |
| `/api/generate` | `POST` | Generates 2D map matrix JSON | `{"seed": 42, "width": 20, "height": 20}` | `{"matrix": [[1,0...]], "seed": 42}` |
| `/api/export` | `POST` | Generates downloadable PNG image | `{"seed": 42, "width": 20, "height": 20}` | Binary PNG download file |

---

## 📂 Subsystem File Overview

| File / Folder | Purpose |
| :--- | :--- |
| 📄 [`app.py`](file:///e:/Projects/PBL/Map%20Gen/backend/app.py) | Main Flask server application containing API endpoints and CORS configuration. |
| 📄 [`__init__.py`](file:///e:/Projects/PBL/Map%20Gen/backend/__init__.py) | Package file for module imports. |
| 📂 [`algorithms/`](file:///e:/Projects/PBL/Map%20Gen/backend/algorithms/ALGORITHM_DESIGNER_ROLE.md) | Module containing procedural map generation algorithms. |
| 📂 [`export/`](file:///e:/Projects/PBL/Map%20Gen/backend/export/EXPORTER_ENGINEER_ROLE.md) | Module handling PNG rendering and image generation. |

---

## 🎮 How to Run

Start the backend server from the project root:
```bash
python backend/app.py
```
The server will run locally at `http://127.0.0.1:5000`.
