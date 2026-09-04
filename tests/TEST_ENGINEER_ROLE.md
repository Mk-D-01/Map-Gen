# 🧪 Test Engineer Role Guide — Automated Test Suite

**Role**: Test Automation & QA Engineer  
**Scope**: Pytest Test Automation, WSGI Mock Fixtures, Seed Determinism Verification, Binary Header Checks  
**Primary Directory**: [`tests/`](file:///e:/Projects/PBL/Map%20Gen/tests/TEST_ENGINEER_ROLE.md)

---

## 🔬 How It Works Under the Hood

The automated test suite uses `pytest` and `pytest-flask` to verify that map generation algorithms, API routes, and image exporters work correctly without bugs.

```
                                +-----------------------------------+
                                |        Pytest Test Runner         |
                                +-----------------------------------+
                                                  |
                        +-------------------------+-------------------------+
                        v                                                   v
             +--------------------+                              +--------------------+
             | conftest.py        |                              | test_prototype.py  |
             | (Shared Fixtures & |                              | (Determinism & API |
             | WSGI Test Client)  |                              | Test Suite)        |
             +--------------------+                              +--------------------+
```

### 1. Pytest Fixture Setup (`conftest.py`)
- Located in [`conftest.py`](file:///e:/Projects/PBL/Map%20Gen/tests/conftest.py).
- **`flask_client` Fixture**: Creates an in-memory Flask test client. This allows unit tests to make real API HTTP calls to endpoints (`/health`, `/api/generate`, `/api/export`) without needing to launch a background web server process.
- **`generator` & `exporter` Fixtures**: Supply pre-configured generator and exporter instances for test functions.

### 2. Test Verification Checks (`test_prototype.py`)
Located in [`test_prototype.py`](file:///e:/Projects/PBL/Map%20Gen/tests/test_prototype.py):

1. **Seed Determinism Check (`TestSeedReproducibility`)**:
   Generates two map grids using identical seed numbers (`seed=42`) and asserts that both 2D arrays are identical. Confirms that using a different seed (`99`) produces a different map layout.
2. **Dimensions & Cell State Validation (`TestGridDimensions`, `TestCellValues`)**:
   Verifies that the generated matrix matches the requested `width` and `height`, and asserts that every cell value is strictly a valid wall (`1`) or floor (`0`).
3. **API & PNG Export Checks (`TestEndpoints`)**:
   - Sends requests to `/api/generate` and checks for HTTP `200 OK` status and valid JSON.
   - Sends requests to `/api/export` and verifies that the output starts with standard PNG magic header bytes (`b"\x89PNG"`).

---

## 📂 Subsystem File Overview

| File | Component | Purpose |
| :--- | :--- | :--- |
| 📄 [`conftest.py`](file:///e:/Projects/PBL/Map%20Gen/tests/conftest.py) | Pytest Fixtures | Sets up mock Flask clients, generator fixtures, and exporter instances. |
| 📄 [`test_prototype.py`](file:///e:/Projects/PBL/Map%20Gen/tests/test_prototype.py) | Test Suite | Contains unit tests covering seed reproducibility, dimensions, cell validity, REST routes, and PNG export. |
| 📄 [`__init__.py`](file:///e:/Projects/PBL/Map%20Gen/tests/__init__.py) | Package File | Enables pytest package discovery. |

---

## 💻 How to Run Tests

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
