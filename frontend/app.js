/**
 * MapGen Engine — Frontend Application (OOP / ES6 Class)
 *
 * Encapsulates all canvas rendering, API communication, and UI state
 * management inside a single `MapGenApp` class.
 *
 * OOP Principles:
 *   - Encapsulation:  DOM references, state, and helpers are private.
 *   - SRP:            Separate methods for API calls, rendering, and UI updates.
 */

"use strict";

class MapGenApp {
  // ── Static configuration ────────────────────────────────────────
  static API_BASE = "http://localhost:5000";
  static CELL_SIZE = 20;
  static WALL_COLOR = "#0a0a0f";
  static FLOOR_COLOR = "#f7f4ef";
  static GRID_LINE_COLOR = "rgba(224, 109, 83, 0.08)";

  /**
   * Create a MapGenApp and bind it to the DOM elements.
   * @param {string} canvasId - The id of the <canvas> element.
   */
  constructor(canvasId) {
    // ── Canvas ────────────────────────────────────────────────────
    this._canvas = document.getElementById(canvasId);
    this._ctx = this._canvas.getContext("2d");

    // ── DOM refs ──────────────────────────────────────────────────
    this._seedInput = document.getElementById("seedInput");
    this._widthInput = document.getElementById("widthInput");
    this._heightInput = document.getElementById("heightInput");
    this._generateBtn = document.getElementById("generateBtn");
    this._downloadBtn = document.getElementById("downloadBtn");
    this._statusBar = document.getElementById("statusBar");
    this._canvasWrapper = document.getElementById("canvasWrapper");
    this._canvasPlaceholder = document.getElementById("canvasPlaceholder");
    this._canvasMeta = document.getElementById("canvasMeta");

    // ── State ─────────────────────────────────────────────────────
    this._lastMatrix = null;
    this._isLoading = false;

    // ── Initialise ────────────────────────────────────────────────
    this._bindEvents();
  }

  // ──────────────────────────────────────────────────────────────────
  //  PUBLIC METHODS
  // ──────────────────────────────────────────────────────────────────

  /**
   * Request a new map from the Flask API and render it on the canvas.
   * @param {number} seed
   * @param {number} width
   * @param {number} height
   */
  async generateMap(seed, width, height) {
    if (this._isLoading) return;
    this._setLoading(true);
    this._setStatus("Generating map…", "");

    try {
      const response = await fetch(`${MapGenApp.API_BASE}/api/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ seed, width, height }),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.error || `HTTP ${response.status}`);
      }

      const data = await response.json();
      this._lastMatrix = data.matrix;

      this.renderGrid(data.matrix);

      const elapsed = performance.now();
      this._setStatus(
        `✓ Generated — Seed ${data.seed} · ${width}×${height} · ${width * height} cells`,
        "success"
      );
      this._downloadBtn.disabled = false;
    } catch (err) {
      this._setStatus(`✗ Error: ${err.message}`, "error");
      console.error("MapGenApp.generateMap error:", err);
    } finally {
      this._setLoading(false);
    }
  }

  /**
   * Draw a 2-D matrix on the canvas as coloured rectangles.
   * @param {number[][]} matrix - 2-D array of 0s and 1s.
   */
  renderGrid(matrix) {
    const rows = matrix.length;
    const cols = rows > 0 ? matrix[0].length : 0;
    const cellSize = MapGenApp.CELL_SIZE;

    // Resize canvas to fit the grid
    this._canvas.width = cols * cellSize;
    this._canvas.height = rows * cellSize;

    // Show the canvas, hide placeholder
    this._canvas.style.display = "block";
    this._canvasPlaceholder.style.display = "none";
    this._canvasWrapper.classList.add("has-content");

    // Draw cells
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < cols; x++) {
        const cell = matrix[y][x];
        this._ctx.fillStyle =
          cell === 1 ? MapGenApp.WALL_COLOR : MapGenApp.FLOOR_COLOR;
        this._ctx.fillRect(
          x * cellSize,
          y * cellSize,
          cellSize,
          cellSize
        );
      }
    }

    // Draw subtle grid lines for clarity
    this._ctx.strokeStyle = MapGenApp.GRID_LINE_COLOR;
    this._ctx.lineWidth = 0.5;
    for (let y = 0; y <= rows; y++) {
      this._ctx.beginPath();
      this._ctx.moveTo(0, y * cellSize);
      this._ctx.lineTo(cols * cellSize, y * cellSize);
      this._ctx.stroke();
    }
    for (let x = 0; x <= cols; x++) {
      this._ctx.beginPath();
      this._ctx.moveTo(x * cellSize, 0);
      this._ctx.lineTo(x * cellSize, rows * cellSize);
      this._ctx.stroke();
    }

    // Update metadata display
    this._canvasMeta.textContent = `${cols}×${rows} · ${cols * rows} cells`;
  }

  /**
   * Request a PNG export from the API and trigger a browser download.
   * @param {number} seed
   * @param {number} width
   * @param {number} height
   */
  async downloadPNG(seed, width, height) {
    if (this._isLoading) return;
    this._setLoading(true, "download");
    this._setStatus("Exporting PNG…", "");

    try {
      const response = await fetch(`${MapGenApp.API_BASE}/api/export`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ seed, width, height }),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.error || `HTTP ${response.status}`);
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      // Programmatic download
      const a = document.createElement("a");
      a.href = url;
      a.download = `mapgen_seed${seed}_${width}x${height}.png`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);

      this._setStatus(`✓ PNG downloaded — mapgen_seed${seed}_${width}x${height}.png`, "success");
    } catch (err) {
      this._setStatus(`✗ Export error: ${err.message}`, "error");
      console.error("MapGenApp.downloadPNG error:", err);
    } finally {
      this._setLoading(false);
    }
  }

  // ──────────────────────────────────────────────────────────────────
  //  PRIVATE METHODS
  // ──────────────────────────────────────────────────────────────────

  /** Wire up click events on UI controls. */
  _bindEvents() {
    this._generateBtn.addEventListener("click", () => {
      const seed = parseInt(this._seedInput.value, 10) || 42;
      const width = parseInt(this._widthInput.value, 10) || 20;
      const height = parseInt(this._heightInput.value, 10) || 20;
      this.generateMap(seed, width, height);
    });

    this._downloadBtn.addEventListener("click", () => {
      const seed = parseInt(this._seedInput.value, 10) || 42;
      const width = parseInt(this._widthInput.value, 10) || 20;
      const height = parseInt(this._heightInput.value, 10) || 20;
      this.downloadPNG(seed, width, height);
    });

    // Allow Enter key to trigger generation
    const inputs = [this._seedInput, this._widthInput, this._heightInput];
    inputs.forEach((input) => {
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
          this._generateBtn.click();
        }
      });
    });
  }

  /**
   * Toggle loading state on buttons.
   * @param {boolean} loading
   * @param {string}  [which="generate"] - "generate" or "download"
   */
  _setLoading(loading, which = "generate") {
    this._isLoading = loading;
    const btn =
      which === "download" ? this._downloadBtn : this._generateBtn;

    if (loading) {
      btn.classList.add("loading");
      btn.disabled = true;
    } else {
      btn.classList.remove("loading");
      btn.disabled = false;
      // Keep download disabled if no map has been generated
      if (!this._lastMatrix) {
        this._downloadBtn.disabled = true;
      }
    }
  }

  /**
   * Display a message in the status bar.
   * @param {string} message
   * @param {string} type - "", "success", or "error"
   */
  _setStatus(message, type) {
    this._statusBar.textContent = message;
    this._statusBar.className = "status-bar visible";
    if (type) {
      this._statusBar.classList.add(type);
    }
  }
}

// ── Bootstrap ─────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  window.mapGenApp = new MapGenApp("mapCanvas");
});
