Key principles:

Minimal stack: No build step, no databases, no ORM. Just Flask + PIL + Perlin noise.
Modular: Each person's code is isolated (algorithms don't know about Flask, export doesn't know about algorithms).
Testable: Every module has unit tests; CI catches bugs before merge.
Portfolio-ready: Clear README, documented APIs, clean git history.
Easy to migrate: Swap out Flask for FastAPI, Vanilla JS for React, PIL for Sharp — the algorithm core stays the same.


1. Project Lead / DevOps (Niche: Infrastructure & coordination)

Tech stack: Docker, Docker Compose, GitHub Actions, shell scripting
Owns: Dockerfile, docker-compose.yml, .github/workflows/, repo structure

Deliverables:

Set up git repo with branch protection rules:
main: require PR review + CI pass before merge
Feature branches: feature/*, fix/*, docs/* for team members
PR template with checklist (code review, tests, docs)
Dockerfile for containerised Flask app
docker-compose.yml for local dev (Flask + mocked DB)
.gitignore: Python (__pycache__, .venv, *.pyc), build artifacts
GitHub Actions workflow: linting (flake8) + unit tests on every PR
CONTRIBUTING.md: branch naming, commit message style, PR process


2. Backend Lead (Niche: Flask architecture & API design)

Tech stack: Flask, Python 3.9+, JSON, HTTP
Owns: /backend/app.py, /backend/api/, request/response contracts

Deliverables:

/backend/app.py: Flask app init, CORS, error handlers
/backend/api/routes/:
generate.py: POST /api/generate → calls algorithm module, returns tiles JSON
export.py: POST /api/export/image + /api/export/json
health.py: GET /health for DevOps monitoring
/backend/requirements.txt:

  Flask==2.3.0
  Flask-CORS==4.0.0
  Pillow==9.5.0
  noise==1.2.2

/backend/config.py: Constants (tile sizes, max dimensions, rate limits)
/backend/tests/test_api.py: Unit tests for all routes (pytest)



Interface with #3 (Algorithm Dev):

3. Algorithm Developer (Niche: Procedural generation logic)

Tech stack: NumPy, Perlin noise library, Python
Owns: /backend/algorithms/, pure tile generation

Deliverables:

/backend/algorithms/perlin.py:
python
  def generate_perlin(width, height, scale, octaves, persistence, lacunarity, seed):
      # Return: 2D array of tiles
      return [[{'type': 'grass', 'value': 0.6}, ...], ...]
/backend/algorithms/cellular.py: Cellular automata (caves)
/backend/algorithms/bsp.py: Binary space partition (dungeons)
Each returns consistent format: 2D list of dicts with type and value keys
/backend/algorithms/tests/: Unit tests for each algorithm (seed reproducibility, edge cases)
/backend/ALGORITHMS.md: How each works, parameters, example outputs

Critical: No Flask imports in algorithm modules. Pure Python functions only — backend calls them.



4. Image & Export Developer (Niche: Data serialization & visualization)

Tech stack: Pillow (PIL), JSON, Python
Owns: /backend/export/, file I/O

Deliverables:

/backend/export/image.py:
=
/backend/export/json.py:




5. Frontend Developer (Niche: UI/UX, Vanilla JS)

Tech stack: HTML, CSS, Vanilla JS (no framework), Fetch API
Owns: /frontend/, user-facing interactions

Deliverables:

/frontend/index.html: Single-page layout
/frontend/css/style.css: Clean, minimal design (no framework)
/frontend/js/main.js:
Fetch /api/generate on button click
Render preview canvas
Handle downloads
/frontend/js/preview.js: Canvas rendering logic (map tiles to pixels)
Tests: Mock API, verify UI updates on response

No build step. Serve files directly from Flask static/ folder.



6. QA / Testing / Documentation (Niche: Quality assurance & knowledge transfer)

Tech stack: pytest, pytest-cov, Markdown, GitHub wiki
Owns: /tests/, /docs/, quality gates

Deliverables:

/tests/integration/test_full_pipeline.py:
Hit /api/generate → verify response shape
Hit /api/export/image → verify PNG valid
Hit /api/export/json → verify JSON parseable
/tests/e2e/: Selenium/Playwright (optional) for frontend interactions
/docs/:
SETUP.md: "Clone repo → docker-compose up → open localhost:5000"
API.md: Full endpoint docs, request/response examples
ARCHITECTURE.md: System diagram, role overview
ALGORITHMS.md: Linked from #3, expanded with visualizations
/README.md: Project description, quick start, portfolio blurb
CI coverage report: pytest --cov=backend


Commit message convention (keep it simple):

feat: add X — new feature
fix: resolve X — bug fix
docs: update X — documentation
test: add tests for X — tests only
refactor: improve X — code quality
chore: update deps — maintenance