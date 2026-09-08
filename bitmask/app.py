import os
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def generate_procedural_grid(width=16, height=10, fill_prob=0.45):
    """Generates a binary grid (1 = Terrain/Grass, 0 = Water/Void)."""
    grid = [[0 for _ in range(width)] for _ in range(height)]
    
    for y in range(height):
        for x in range(width):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                grid[y][x] = 0
            else:
                grid[y][x] = 1 if random.random() < fill_prob else 0
                
    smoothed = [row[:] for row in grid]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            neighbors = sum(
                grid[y + dy][x + dx]
                for dy in [-1, 0, 1]
                for dx in [-1, 0, 1]
                if not (dx == 0 and dy == 0)
            )
            smoothed[y][x] = 1 if neighbors >= 4 else 0
            
    return smoothed

def calculate_bitmask(grid, x, y):
    height = len(grid)
    width = len(grid[0])
    
    if grid[y][x] == 0:
        return None

    mask = 0
    if y > 0 and grid[y - 1][x] == 1: mask |= 1
    if x < width - 1 and grid[y][x + 1] == 1: mask |= 2
    if y < height - 1 and grid[y + 1][x] == 1: mask |= 4
    if x > 0 and grid[y][x - 1] == 1: mask |= 8

    return mask

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    bitmask_mapping = data.get("mapping", {})
    
    # 16x10 tiles at 64x64 fits a standard 1024x640 canvas
    map_w, map_h = 16, 10
    grid = generate_procedural_grid(map_w, map_h)
    
    level_map = []
    for y in range(map_h):
        row = []
        for x in range(map_w):
            if grid[y][x] == 1:
                mask = calculate_bitmask(grid, x, y)
                tile_info = bitmask_mapping.get(str(mask), None)
                row.append({"type": "terrain", "mask": mask, "tile": tile_info})
            else:
                row.append({"type": "water", "mask": None, "tile": None})
        level_map.append(row)
        
    return jsonify({"grid": level_map, "width": map_w, "height": map_h})

if __name__ == "__main__":
    app.run(debug=True, port=5000)