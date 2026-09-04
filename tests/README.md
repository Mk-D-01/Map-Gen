# 🧪 Tests Module — Automated Testing Suite

Welcome to the **Tests** directory! This directory houses the Pytest test suite, fixtures, and assertions that guarantee MapGen Engine runs perfectly without bugs.

---

## 🧒 Explain Like I'm 5 (ELI5)

> Imagine a team of **Inspector Robots**:
>
> 1. **Seed Inspector** (`TestSeedReproducibility`): Asks for map seed 42 twice. If the maps aren't 100% identical twin sisters, it rings an alarm! 🚨
> 2. **Ruler Inspector** (`TestGridDimensions`): Measures the map grid with a ruler. If you asked for a 20×20 grid, it double-checks every single row and column! 📐
> 3. **Color Inspector** (`TestCellValues`): Inspects every tile to ensure only wall (`1`) or floor (`0`) blocks exist (no purple monsters allowed)! 🎨
> 4. **API Inspector** (`TestHealthEndpoint`, `TestGenerateEndpoint`, `TestExportEndpoint`): Knocks on the backend server door and verifies that map data and PNG picture downloads arrive quickly! 📬

---

## ⚙️ How It Works & Methodology

The test suite uses `pytest` and `pytest-flask` to execute automated unit and integration tests:

- **Pytest Fixtures (`conftest.py`)**:
  - `flask_client`: Creates a test client for `MapGenApp` without needing to run an external web server process.
  - `generator`: Supplies pre-configured `PrototypeGridGenerator(seed=42)` instances.
  - `exporter`: Supplies `PNGExporter` instances for image output checks.
- **Determinism & Reproducibility Assertions**:
  - Validates that pseudo-random number generator (PRNG) seeds guarantee identical outputs (`grid1 == grid2`).
- **Binary Content Validation**:
  - Inspects PNG binary headers (`b"\x89PNG"`) returned by `/api/export` to ensure valid image encoding.

---

## 📂 Files in This Directory

| File | Component | Description |
| :--- | :--- | :--- |
| 📄 [`conftest.py`](file:///e:/Projects/PBL/Map%20Gen/tests/conftest.py) | Pytest Fixtures | Sets up shared test fixtures, mock Flask clients, and default generators. |
| 📄 [`test_prototype.py`](file:///e:/Projects/PBL/Map%20Gen/tests/test_prototype.py) | Test Suite | Unit tests covering seed reproducibility, dimensions, cell validity, REST endpoints, and PNG export. |
| 📄 [`__init__.py`](file:///e:/Projects/PBL/Map%20Gen/tests/__init__.py) | Package Init | Enables pytest package discovery. |

---

## 🎮 How to Run Tests

Run pytest from the root folder:
```bash
pytest tests/
```
To run with detailed verbose output:
```bash
pytest -v tests/
```
To run a specific test class:
```bash
pytest tests/test_prototype.py::TestSeedReproducibility -v
```
