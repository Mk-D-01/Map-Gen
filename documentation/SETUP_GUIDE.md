# MapGen Engine — Setup Guide

A step-by-step guide to install, run, and test the MapGen Prototype locally.

---

## Prerequisites

| Tool   | Version  | Check command        |
|--------|----------|----------------------|
| Python | ≥ 3.10   | `python --version`   |
| pip    | latest   | `pip --version`      |
| Git    | any      | `git --version`      |

---

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Map\ Gen
```

---

## 2. Create & Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Flask** + **flask-cors** — REST API server
- **Pillow** — PNG image export
- **pytest** — Test framework

---

## 4. Run the Flask Backend

```bash
python -m backend.app
```

You should see:
```
🗺️  MapGen Engine API running on http://localhost:5000
```

### Quick Health Check

Open a new terminal and run:
```bash
curl http://localhost:5000/health
```
Expected response: `{"status": "ok"}`

---

## 5. Open the Frontend

While the Flask server is running, open the frontend in your browser:

```
frontend/index.html
```

> **Note:** Open the HTML file directly in your browser (File → Open), or use a
> local HTTP server like `python -m http.server 8080 --directory frontend` and
> visit `http://localhost:8080`.

### Usage
1. Enter a **Seed** number (default: 42).
2. Set the **Width** and **Height** (default: 20 × 20).
3. Click **"⚡ Generate Prototype Map"**.
4. The canvas will display the cave map (black = wall, white = floor).
5. Click **"⬇ Download PNG"** to save the map as a PNG image.

---

## 6. Run the Test Suite

```bash
python -m pytest tests/ -v
```

Expected output:
```
tests/test_prototype.py::TestSeedReproducibility::test_seed_reproducibility     PASSED
tests/test_prototype.py::TestSeedReproducibility::test_different_seeds_differ    PASSED
tests/test_prototype.py::TestGridDimensions::test_default_dimensions             PASSED
tests/test_prototype.py::TestGridDimensions::test_custom_dimensions              PASSED
tests/test_prototype.py::TestCellValues::test_cells_are_binary                   PASSED
tests/test_prototype.py::TestHealthEndpoint::test_health_check                   PASSED
tests/test_prototype.py::TestGenerateEndpoint::test_generate_returns_matrix      PASSED
tests/test_prototype.py::TestGenerateEndpoint::test_generate_bad_dimensions      PASSED
tests/test_prototype.py::TestExportEndpoint::test_export_returns_png             PASSED
tests/test_prototype.py::TestPNGExporter::test_export_to_bytes                   PASSED
```

---

## Project Structure

```
Map Gen/
├── backend/
│   ├── __init__.py               # Backend package
│   ├── app.py                    # Flask app (MapGenApp class)
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── base.py               # Abstract BaseGridGenerator
│   │   └── prototype_gen.py      # PrototypeGridGenerator (cellular automata)
│   └── export/
│       ├── __init__.py
│       ├── base_exporter.py      # Abstract BaseExporter
│       └── prototype_export.py   # PNGExporter (Pillow)
├── frontend/
│   ├── index.html                # Web UI
│   ├── style.css                 # Warm terracotta dark theme
│   └── app.js                    # MapGenApp JS class
├── tests/
│   ├── conftest.py               # Pytest fixtures
│   └── test_prototype.py         # Test suite
├── documentation/
│   └── SETUP_GUIDE.md            # ← You are here
├── requirements.txt
└── .gitignore
```

---

## OOP Architecture

```
BaseGridGenerator (ABC)
  └── PrototypeGridGenerator    ← cellular automata + smoothing

BaseExporter (ABC)
  └── PNGExporter               ← Pillow pixel rendering

MapGenApp                       ← Flask factory with dependency injection
```

All algorithms and export formats extend abstract base classes, making the
engine **open for extension, closed for modification** (Open/Closed Principle).
