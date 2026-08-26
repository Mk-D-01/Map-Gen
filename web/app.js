/* ==========================================================================
   MapGen Web - Interactive Application Engine (DSA & Procedural Core)
   ========================================================================== */

(function () {
  'use strict';

  // --- Global Constants & Color Palettes ---
  const PALETTE = {
    water: { r: 75, g: 85, b: 135, a: 255, hex: '#4b5587' },
    sand: { r: 210, g: 190, b: 140, a: 255, hex: '#d2be8c' },
    meadow: { r: 145, g: 185, b: 110, a: 255, hex: '#91b96e' },
    forest: { r: 80, g: 135, b: 85, a: 255, hex: '#508755' },
    dot: { r: 20, g: 25, b: 20, a: 255, hex: '#141914' },
    void: { r: 22, g: 20, b: 28, a: 255, hex: '#16141c' },
    wall: { r: 50, g: 45, b: 60, a: 255, hex: '#322d3c' },
    floor: { r: 210, g: 190, b: 140, a: 255, hex: '#d2be8c' },
    corridor: { r: 180, g: 160, b: 120, a: 255, hex: '#b4a078' }
  };

  // --- 1. Pure Mathematical & DSA Helper Functions ---
  
  /** Bitwise Spatial Integer Hash (Matches map_gen_image.c) */
  function Hash(x, y, seed) {
    let n = (x + y * 57 + seed * 131) | 0;
    n = ((n << 13) ^ n) | 0;
    const term = Math.imul(n, Math.imul(n, n) * 15731 + 789221) + 1376312589;
    return 1.0 - ((term & 0x7fffffff) / 1073741824.0);
  }

  /** Linear Interpolation */
  function Lerp(a, b, t) {
    return a + t * (b - a);
  }

  /** Quintic Hermite Fade Curve: t^3 * (t * (t * 6 - 15) + 10) */
  function SmoothFade(t) {
    return t * t * t * (t * (t * 6 - 15) + 10);
  }

  /** 2D Smooth Value Noise Generator */
  function SmoothNoise2D(x, y, seed) {
    const X = Math.floor(x);
    const Y = Math.floor(y);
    const xf = x - X;
    const yf = y - Y;

    const u = SmoothFade(xf);
    const v = SmoothFade(yf);

    const n00 = (Hash(X, Y, seed) + 1.0) * 0.5;
    const n10 = (Hash(X + 1, Y, seed) + 1.0) * 0.5;
    const n01 = (Hash(X, Y + 1, seed) + 1.0) * 0.5;
    const n11 = (Hash(X + 1, Y + 1, seed) + 1.0) * 0.5;

    const x1 = Lerp(n00, n10, u);
    const x2 = Lerp(n01, n11, u);

    return Lerp(x1, x2, v);
  }

  // --- 2. Procedural Generators Engine ---

  /** Generator A: Perlin / Smooth Noise Map (Terrain & Biomes) */
  function generateNoiseMap(width, height, gridSize, seed, scale, octaves, roughness) {
    const gridW = Math.ceil(width / gridSize);
    const gridH = Math.ceil(height / gridSize);
    const matrix = [];

    for (let y = 0; y < gridH; y++) {
      const row = [];
      for (let x = 0; x < gridW; x++) {
        let n = 0;
        let freq = scale;
        let amp = 1.0;
        let maxAmp = 0;

        for (let o = 0; o < octaves; o++) {
          n += SmoothNoise2D(x * freq, y * freq, seed + o * 100) * amp;
          maxAmp += amp;
          freq *= 2.0;
          amp *= roughness;
        }

        n /= maxAmp;

        let tileType = 'water';
        let color = PALETTE.water;

        if (n >= 0.42 && n < 0.48) {
          tileType = 'sand';
          color = PALETTE.sand;
        } else if (n >= 0.48 && n < 0.62) {
          tileType = 'meadow';
          color = PALETTE.meadow;
        } else if (n >= 0.62) {
          tileType = 'forest';
          color = PALETTE.forest;
        }

        // Dot scatter on land
        let hasDetail = false;
        if (tileType !== 'water') {
          const dotHash = Math.abs((x * 739221 + y * 1376312589 + seed) % 100);
          if (dotHash < 5) hasDetail = true;
        }

        row.push({ x, y, val: n, type: tileType, color, hasDetail });
      }
      matrix.push(row);
    }

    return { gridW, gridH, matrix };
  }

  /** Generator B: Cellular Automata Cave Engine (Corrected 4-5 Rule with Hysteresis) */
  function generateCellularAutomata(width, height, gridSize, seed, fillProb, iterations) {
    const gridW = Math.ceil(width / gridSize);
    const gridH = Math.ceil(height / gridSize);
    let map = [];

    // Step 1: Initial Seed Pass (Random distribution with solid boundary border)
    for (let y = 0; y < gridH; y++) {
      const row = [];
      for (let x = 0; x < gridW; x++) {
        if (x === 0 || x === gridW - 1 || y === 0 || y === gridH - 1) {
          row.push(1); // 1 = Solid Wall Boundary
        } else {
          // Normalize Hash output to [0, 1]
          const h = (Hash(x, y, seed) + 1.0) * 0.5;
          row.push(h < fillProb ? 1 : 0); // 1 = Wall, 0 = Floor
        }
      }
      map.push(row);
    }

    // Step 2: Iterative Smoothing Passes via 4-5 Rule with State Hysteresis
    for (let it = 0; it < iterations; it++) {
      const newMap = [];
      for (let y = 0; y < gridH; y++) {
        const newRow = [];
        for (let x = 0; x < gridW; x++) {
          // Keep outer border strictly wall
          if (x === 0 || x === gridW - 1 || y === 0 || y === gridH - 1) {
            newRow.push(1);
          } else {
            // Count 8 surrounding Moore neighbors (treating out-of-bounds as wall)
            let wallCount = 0;
            for (let dy = -1; dy <= 1; dy++) {
              for (let dx = -1; dx <= 1; dx++) {
                if (dx === 0 && dy === 0) continue;
                const nx = x + dx;
                const ny = y + dy;
                if (nx < 0 || nx >= gridW || ny < 0 || ny >= gridH) {
                  wallCount++;
                } else if (map[ny][nx] === 1) {
                  wallCount++;
                }
              }
            }

            // Standard 4-5 Rule:
            // > 4 neighbors: becomes Wall
            // < 4 neighbors: becomes Floor
            // == 4 neighbors: retains existing state (Hysteresis prevents collapsing)
            const currentVal = map[y][x];
            if (wallCount > 4) {
              newRow.push(1);
            } else if (wallCount < 4) {
              newRow.push(0);
            } else {
              newRow.push(currentVal);
            }
          }
        }
        newMap.push(newRow);
      }
      map = newMap;
    }

    // Step 3: Flood Fill Cave Pocket Cleanup (Fill isolated unplayable cavities)
    const visited = Array.from({ length: gridH }, () => Array(gridW).fill(false));
    let largestCave = [];

    for (let y = 1; y < gridH - 1; y++) {
      for (let x = 1; x < gridW - 1; x++) {
        if (map[y][x] === 0 && !visited[y][x]) {
          const currentCave = [];
          const queue = [{ x, y }];
          visited[y][x] = true;

          while (queue.length > 0) {
            const curr = queue.shift();
            currentCave.push(curr);

            const neighbors = [
              { x: curr.x + 1, y: curr.y },
              { x: curr.x - 1, y: curr.y },
              { x: curr.x, y: curr.y + 1 },
              { x: curr.x, y: curr.y - 1 }
            ];

            for (const n of neighbors) {
              if (n.x > 0 && n.x < gridW - 1 && n.y > 0 && n.y < gridH - 1) {
                if (map[n.y][n.x] === 0 && !visited[n.y][n.x]) {
                  visited[n.y][n.x] = true;
                  queue.push(n);
                }
              }
            }
          }

          if (currentCave.length > largestCave.length) {
            largestCave = currentCave;
          }
        }
      }
    }

    // Fill small isolated pockets (keep only the largest connected cave region)
    if (largestCave.length > 0) {
      const caveSet = new Set(largestCave.map(p => `${p.x},${p.y}`));
      for (let y = 1; y < gridH - 1; y++) {
        for (let x = 1; x < gridW - 1; x++) {
          if (map[y][x] === 0 && !caveSet.has(`${x},${y}`)) {
            map[y][x] = 1; // Convert isolated open space into wall
          }
        }
      }
    }

    // Convert map matrix to renderable tile structure
    const matrix = [];
    for (let y = 0; y < gridH; y++) {
      const row = [];
      for (let x = 0; x < gridW; x++) {
        const isWall = map[y][x] === 1;
        row.push({
          x, y,
          type: isWall ? 'wall' : 'floor',
          color: isWall ? PALETTE.wall : PALETTE.meadow,
          hasDetail: false
        });
      }
      matrix.push(row);
    }

    return { gridW, gridH, matrix };
  }

  /** Generator C: Binary Space Partitioning (BSP Trees - Dungeons) */
  function generateBSPDungeon(width, height, gridSize, seed, minRoomSize) {
    const gridW = Math.ceil(width / gridSize);
    const gridH = Math.ceil(height / gridSize);
    
    // Initialize void matrix
    const grid = Array.from({ length: gridH }, () => Array(gridW).fill(0)); // 0 = void wall, 1 = room floor, 2 = corridor

    // BSP Tree Node Definition
    class BSPNode {
      constructor(x, y, w, h) {
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.leftChild = null;
        this.rightChild = null;
        this.room = null;
      }

      split(minSize, seedVal) {
        if (this.leftChild || this.rightChild) return false;

        // Determine split direction (horizontal or vertical)
        let splitH = false;
        if (this.w / this.h >= 1.25) splitH = false;
        else if (this.h / this.w >= 1.25) splitH = true;
        else splitH = (Hash(this.x, this.y, seedVal) > 0);

        const max = (splitH ? this.h : this.w) - minSize;
        if (max <= minSize) return false;

        // Calculate split point
        const splitPos = Math.floor(Lerp(minSize, max, (Hash(this.x + 3, this.y + 7, seedVal) + 1) * 0.5));

        if (splitH) {
          this.leftChild = new BSPNode(this.x, this.y, this.w, splitPos);
          this.rightChild = new BSPNode(this.x, this.y + splitPos, this.w, this.h - splitPos);
        } else {
          this.leftChild = new BSPNode(this.x, this.y, splitPos, this.h);
          this.rightChild = new BSPNode(this.x + splitPos, this.y, this.w - splitPos, this.h);
        }
        return true;
      }

      createRooms(minSize, seedVal) {
        if (this.leftChild || this.rightChild) {
          if (this.leftChild) this.leftChild.createRooms(minSize, seedVal + 1);
          if (this.rightChild) this.rightChild.createRooms(minSize, seedVal + 2);
        } else {
          // Leaf node: carve room inside bounds
          const rw = Math.max(3, Math.floor(this.w * 0.7));
          const rh = Math.max(3, Math.floor(this.h * 0.7));
          const rx = this.x + Math.floor((this.w - rw) / 2);
          const ry = this.y + Math.floor((this.h - rh) / 2);
          this.room = { x: rx, y: ry, w: rw, h: rh, cx: Math.floor(rx + rw / 2), cy: Math.floor(ry + rh / 2) };

          for (let py = ry; py < ry + rh; py++) {
            for (let px = rx; px < rx + rw; px++) {
              if (py > 0 && py < gridH - 1 && px > 0 && px < gridW - 1) {
                grid[py][px] = 1;
              }
            }
          }
        }
      }

      getRoomCentroids() {
        if (this.room) return [this.room];
        let rooms = [];
        if (this.leftChild) rooms = rooms.concat(this.leftChild.getRoomCentroids());
        if (this.rightChild) rooms = rooms.concat(this.rightChild.getRoomCentroids());
        return rooms;
      }
    }

    const root = new BSPNode(1, 1, gridW - 2, gridH - 2);
    const nodes = [root];
    
    // Recursive bisection pass
    for (let i = 0; i < 5; i++) {
      const len = nodes.length;
      for (let j = 0; j < len; j++) {
        const node = nodes[j];
        if (node.split(minRoomSize, seed + i * 10 + j)) {
          nodes.push(node.leftChild);
          nodes.push(node.rightChild);
        }
      }
    }

    root.createRooms(minRoomSize, seed);

    // Corridor Connection Pass: Connect leaf room centroids
    const rooms = root.getRoomCentroids();
    for (let i = 0; i < rooms.length - 1; i++) {
      const r1 = rooms[i];
      const r2 = rooms[i + 1];

      let cx = r1.cx;
      let cy = r1.cy;

      while (cx !== r2.cx) {
        if (cy >= 0 && cy < gridH && cx >= 0 && cx < gridW) grid[cy][cx] = 2;
        cx += (r2.cx > cx) ? 1 : -1;
      }
      while (cy !== r2.cy) {
        if (cy >= 0 && cy < gridH && cx >= 0 && cx < gridW) grid[cy][cx] = 2;
        cy += (r2.cy > cy) ? 1 : -1;
      }
    }

    // Convert grid to matrix format
    const matrix = [];
    for (let y = 0; y < gridH; y++) {
      const row = [];
      for (let x = 0; x < gridW; x++) {
        const val = grid[y][x];
        let type = 'void';
        let color = PALETTE.void;

        if (val === 1) {
          type = 'floor';
          color = PALETTE.floor;
        } else if (val === 2) {
          type = 'corridor';
          color = PALETTE.corridor;
        }

        row.push({ x, y, type, color, hasDetail: false });
      }
      matrix.push(row);
    }

    return { gridW, gridH, matrix };
  }

  // --- 3. Canvas Rendering & UI Sync ---

  function renderToCanvas(canvas, genData, gridSize) {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const { gridW, gridH, matrix } = genData;

    canvas.width = gridW * gridSize;
    canvas.height = gridH * gridSize;

    ctx.fillStyle = '#0d0c0f';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (let y = 0; y < gridH; y++) {
      for (let x = 0; x < gridW; x++) {
        const tile = matrix[y][x];
        const c = tile.color;

        ctx.fillStyle = `rgb(${c.r}, ${c.g}, ${c.b})`;
        ctx.fillRect(x * gridSize, y * gridSize, gridSize, gridSize);

        // Scatter detail dot if applicable
        if (tile.hasDetail) {
          ctx.fillStyle = `rgb(${PALETTE.dot.r}, ${PALETTE.dot.g}, ${PALETTE.dot.b})`;
          ctx.fillRect(x * gridSize + Math.floor(gridSize / 2), y * gridSize + Math.floor(gridSize / 2), 1, 1);
        }
      }
    }
  }

  // Toast notification system
  function showToast(message) {
    let toast = document.getElementById('toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'toast';
      toast.className = 'toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
  }

  // --- 4. Application Initialization & Event Listeners ---

  document.addEventListener('DOMContentLoaded', () => {
    // Canvas elements
    const heroCanvas = document.getElementById('heroCanvas');
    const sandboxCanvas = document.getElementById('sandboxCanvas');

    // UI Controls
    const algoSelect = document.getElementById('algoSelect');
    const seedInput = document.getElementById('seedInput');
    const randomSeedBtn = document.getElementById('randomSeedBtn');
    const scaleSlider = document.getElementById('scaleSlider');
    const scaleVal = document.getElementById('scaleVal');
    const octaveSlider = document.getElementById('octaveSlider');
    const octaveVal = document.getElementById('octaveVal');
    const detailSlider = document.getElementById('detailSlider');
    const detailVal = document.getElementById('detailVal');

    const statTiles = document.getElementById('statTiles');
    const statMem = document.getElementById('statMem');
    const statTime = document.getElementById('statTime');

    const downloadPngBtn = document.getElementById('downloadPngBtn');
    const exportJsonBtn = document.getElementById('exportJsonBtn');
    const copySeedBtn = document.getElementById('copySeedBtn');

    let currentGenData = null;

    // 1. Initial Hero Canvas Render
    if (heroCanvas) {
      const heroData = generateNoiseMap(800, 400, 4, 42, 0.04, 2, 0.3);
      renderToCanvas(heroCanvas, heroData, 4);
    }

    // 2. Render Main Sandbox Canvas
    function updateSandbox() {
      if (!sandboxCanvas) return;

      const algo = algoSelect ? algoSelect.value : 'perlin';
      const seed = parseInt(seedInput.value, 10) || 42;
      const scale = parseFloat(scaleSlider.value) || 0.04;
      const octaves = parseInt(octaveSlider.value, 10) || 2;
      const detail = parseInt(detailSlider.value, 10) || 5;

      const width = 800;
      const height = 400;
      const gridSize = 4;

      const startTime = performance.now();

      if (algo === 'perlin') {
        currentGenData = generateNoiseMap(width, height, gridSize, seed, scale, octaves, 0.3);
      } else if (algo === 'cellular') {
        currentGenData = generateCellularAutomata(width, height, gridSize, seed, 0.45, detail);
      } else if (algo === 'bsp') {
        currentGenData = generateBSPDungeon(width, height, gridSize, seed, detail + 3);
      }

      const endTime = performance.now();

      renderToCanvas(sandboxCanvas, currentGenData, gridSize);

      // Update UI stats
      const totalTiles = currentGenData.gridW * currentGenData.gridH;
      if (statTiles) statTiles.textContent = totalTiles.toLocaleString();
      if (statMem) statMem.textContent = `${(totalTiles * 8 / 1024).toFixed(1)} KB`;
      if (statTime) statTime.textContent = `${(endTime - startTime).toFixed(2)} ms`;
    }

    // Event Bindings
    if (algoSelect) algoSelect.addEventListener('change', updateSandbox);
    if (seedInput) seedInput.addEventListener('input', updateSandbox);

    if (randomSeedBtn) {
      randomSeedBtn.addEventListener('click', () => {
        const rand = Math.floor(Math.random() * 100000);
        seedInput.value = rand;
        updateSandbox();
        showToast(`Generated Random Seed: ${rand}`);
      });
    }

    if (scaleSlider && scaleVal) {
      scaleSlider.addEventListener('input', (e) => {
        scaleVal.textContent = parseFloat(e.target.value).toFixed(3);
        updateSandbox();
      });
    }

    if (octaveSlider && octaveVal) {
      octaveSlider.addEventListener('input', (e) => {
        octaveVal.textContent = e.target.value;
        updateSandbox();
      });
    }

    if (detailSlider && detailVal) {
      detailSlider.addEventListener('input', (e) => {
        detailVal.textContent = e.target.value;
        updateSandbox();
      });
    }

    // Export Controls
    if (downloadPngBtn) {
      downloadPngBtn.addEventListener('click', () => {
        if (!sandboxCanvas) return;
        const link = document.createElement('a');
        link.download = `map_seed_${seedInput.value}.png`;
        link.href = sandboxCanvas.toDataURL('image/png');
        link.click();
        showToast('Downloaded Map Image PNG');
      });
    }

    if (exportJsonBtn) {
      exportJsonBtn.addEventListener('click', () => {
        if (!currentGenData) return;
        const jsonStr = JSON.stringify(currentGenData.matrix, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.download = `map_seed_${seedInput.value}.json`;
        link.href = url;
        link.click();
        URL.revokeObjectURL(url);
        showToast('Exported Map Tile Matrix JSON');
      });
    }

    if (copySeedBtn) {
      copySeedBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(seedInput.value);
        showToast(`Copied Seed #${seedInput.value} to Clipboard`);
      });
    }

    // 3. Tab Switcher for Algorithm Walkthrough
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');

        tabButtons.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.style.display = 'none');

        btn.classList.add('active');
        const activeContent = document.getElementById(`tab-${targetTab}`);
        if (activeContent) activeContent.style.display = 'block';
      });
    });

    // Run initial sandbox update
    updateSandbox();
  });

})();
