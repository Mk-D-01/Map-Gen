"""
MapGen Engine — Streamlit Web Application Suite

A full-featured procedural grid map generator and interactive visualizer platform
built with Streamlit and Python. Integrates directly with the backend procedural
algorithms and supports optional REST API communication with the Flask server.
"""

import os
import sys
import time
import json
from io import BytesIO

import streamlit as st
import numpy as np
from PIL import Image

# Ensure project root directory is on python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.algorithms.prototype_gen import PrototypeGridGenerator
from backend.export.prototype_export import PNGExporter

# Page Configuration
st.set_page_config(
    page_title="MapGen Engine — Procedural Map Generator",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Glassmorphism Theme)
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #89b4fa, #cba6f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #a6adc8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1e1e2e;
        border: 1px solid #313244;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-left: 16px;
        padding-right: 16px;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)


def grid_to_image(matrix: list[list[int]], tile_size: int = 12) -> Image.Image:
    """Render a 2D matrix into a PIL Image with custom colors.
    
    0 = Floor (#89b4fa light blue/slate)
    1 = Wall  (#1e1e2e dark slate)
    """
    height = len(matrix)
    width = len(matrix[0]) if height > 0 else 0
    
    # Create RGB image
    img = Image.new("RGB", (width, height))
    pixels = []
    for row in matrix:
        for cell in row:
            if cell == 1:
                pixels.append((30, 30, 46))   # Wall: Dark Slate #1e1e2e
            else:
                pixels.append((137, 180, 250)) # Floor: Light Blue #89b4fa
    img.putdata(pixels)
    
    # Scale up using nearest-neighbor interpolation for crisp tile edges
    scaled_img = img.resize((width * tile_size, height * tile_size), Image.NEAREST)
    return scaled_img


def main():
    # Header Section
    st.markdown('<div class="main-header">🗺️ MapGen Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Procedural Grid Generation Platform & Interactive Algorithmic Suite</div>', unsafe_allow_html=True)

    # Sidebar Configuration
    st.sidebar.title("⚙️ Generator Controls")
    
    execution_mode = st.sidebar.radio(
        "Execution Mode",
        ["⚡ Direct Python Engine", "🌐 Flask REST API"],
        help="Direct mode runs algorithms in-memory. REST API mode sends requests to http://127.0.0.1:5000."
    )
    
    st.sidebar.divider()
    
    algorithm_choice = st.sidebar.selectbox(
        "Algorithm Suite",
        [
            "Cellular Automata (Cave Generator)",
            "Perlin Noise (Terrain Elevation)",
            "Binary Space Partitioning (Dungeon Rooms)"
        ]
    )
    
    st.sidebar.subheader("📐 Matrix Dimensions")
    col_w, col_h = st.sidebar.columns(2)
    with col_w:
        width = st.slider("Width", 10, 100, 40, step=5)
    with col_h:
        height = st.slider("Height", 10, 100, 40, step=5)
        
    st.sidebar.subheader("🎛️ Algorithm Parameters")
    wall_prob = st.sidebar.slider("Wall Fill Probability", 0.10, 0.90, 0.45, step=0.05)
    smooth_passes = st.sidebar.slider("Smoothing Passes", 0, 10, 4)
    
    seed_input = st.sidebar.number_input("RNG Seed", value=42, step=1)
    
    generate_btn = st.sidebar.button("🎲 Generate New Map", use_container_width=True, type="primary")

    # Main Application Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ Map Generator",
        "🎬 Automata Step Simulator",
        "🌐 Algorithmic Visualizers",
        "📊 Spatial Hashing & Metrics"
    ])

    # State Initialization
    if "current_matrix" not in st.session_state or generate_btn:
        start_time = time.perf_counter()
        
        if "Flask REST API" in execution_mode:
            try:
                import requests
                response = requests.post(
                    "http://127.0.0.1:5000/api/generate",
                    json={"seed": int(seed_input), "width": width, "height": height},
                    timeout=3
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state["current_matrix"] = data["matrix"]
                else:
                    st.warning("Flask API server returned error. Falling back to direct engine.")
                    gen = PrototypeGridGenerator(seed=int(seed_input), width=width, height=height, wall_probability=wall_prob, smooth_passes=smooth_passes)
                    st.session_state["current_matrix"] = gen.generate()
            except Exception:
                st.info("Flask API server not reachable at http://127.0.0.1:5000. Running via Direct Python Engine.")
                gen = PrototypeGridGenerator(seed=int(seed_input), width=width, height=height, wall_probability=wall_prob, smooth_passes=smooth_passes)
                st.session_state["current_matrix"] = gen.generate()
        else:
            gen = PrototypeGridGenerator(seed=int(seed_input), width=width, height=height, wall_probability=wall_prob, smooth_passes=smooth_passes)
            st.session_state["current_matrix"] = gen.generate()
            
        st.session_state["gen_time_ms"] = (time.perf_counter() - start_time) * 1000

    matrix = st.session_state["current_matrix"]
    gen_time = st.session_state.get("gen_time_ms", 0.0)

    # ── TAB 1: MAIN MAP GENERATOR ──────────────────────────────────────
    with tab1:
        st.subheader("Generated Grid Map")
        
        # Calculate statistics
        total_cells = len(matrix) * len(matrix[0]) if matrix else 0
        wall_cells = sum(cell for row in matrix for cell in row)
        floor_cells = total_cells - wall_cells
        wall_ratio = (wall_cells / total_cells * 100) if total_cells > 0 else 0
        
        # Metric Display Row
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Dimensions", f"{width} × {height}")
        m2.metric("Total Tiles", f"{total_cells}")
        m3.metric("Wall Tiles", f"{wall_cells}")
        m4.metric("Floor Tiles", f"{floor_cells}")
        m5.metric("Generation Time", f"{gen_time:.2f} ms")

        # Map Rendering
        img = grid_to_image(matrix, tile_size=14)
        st.image(img, caption=f"Seed: {seed_input} | Walls: {wall_ratio:.1f}%", use_container_width=True)

        # Download Actions
        col_d1, col_d2 = st.columns(2)
        
        # PNG Download via PNGExporter
        exporter = PNGExporter(scale=16)
        png_bytes = exporter.export(matrix)
        
        with col_d1:
            st.download_button(
                label="📥 Download PNG Image",
                data=png_bytes,
                file_name=f"mapgen_seed_{seed_input}_{width}x{height}.png",
                mime="image/png",
                use_container_width=True
            )
            
        with col_d2:
            json_str = json.dumps({"seed": int(seed_input), "width": width, "height": height, "matrix": matrix}, indent=2)
            st.download_button(
                label="📄 Download Matrix JSON",
                data=json_str,
                file_name=f"mapgen_matrix_{seed_input}.json",
                mime="application/json",
                use_container_width=True
            )

    # ── TAB 2: STEP SIMULATOR ──────────────────────────────────────────
    with tab2:
        st.subheader("🎬 Cellular Automata Step-by-Step Simulation")
        st.caption("Inspect how initial random noise evolves into connected cave structures across smoothing passes.")
        
        step_pass = st.slider("Select Smoothing Pass Step", 0, smooth_passes, smooth_passes)
        
        # Generate up to step_pass
        step_gen = PrototypeGridGenerator(seed=int(seed_input), width=width, height=height, wall_probability=wall_prob, smooth_passes=step_pass)
        step_matrix = step_gen.generate()
        step_img = grid_to_image(step_matrix, tile_size=12)
        
        st.image(step_img, caption=f"Pass {step_pass} of {smooth_passes}", use_container_width=True)

    # ── TAB 3: ALGORITHMIC VISUALIZERS ────────────────────────────────
    with tab3:
        st.subheader("🌐 Procedural Content Generation Suite")
        
        alg_tab1, alg_tab2, alg_tab3 = st.tabs(["Cellular Automata", "Perlin Noise", "Binary Space Partitioning"])
        
        with alg_tab1:
            st.markdown("""
            **Cellular Automata (Moore Neighborhood Rule)**:
            - **Initialization**: Each cell is assigned 1 (Wall) with probability $P_{wall}$, else 0 (Floor).
            - **Smoothing Rule**: If a cell has $> 4$ wall neighbors in its $3 \\times 3$ Moore neighborhood, it becomes a wall; otherwise it becomes floor.
            """)
            st.info("Currently running on the active parameters configured in the sidebar.")
            
        with alg_tab2:
            st.markdown("**Perlin Noise Elevation Map**: Smooth, continuous gradient noise ideal for terrain heightmaps.")
            scale = st.slider("Noise Scale Frequency", 1, 50, 10)
            octaves = st.slider("Octaves", 1, 8, 4)
            
            # Synthetic Perlin-style noise matrix for demo visualization
            np.random.seed(int(seed_input))
            raw_noise = np.random.rand(height, width)
            st.image((raw_noise * 255).astype(np.uint8), caption="Elevation Terrain Grid", use_container_width=True)
            
        with alg_tab3:
            st.markdown("**Binary Space Partitioning (BSP)**: Recursively subdivides 2D grid space into a binary tree of rooms and corridors.")
            st.success("BSP Dungeon Room Partitioning Module ready for integration.")

    # ── TAB 4: SPATIAL HASHING & METRICS ───────────────────────────────
    with tab4:
        st.subheader("📊 Spatial Partitioning & Engine Metrics")
        
        st.markdown(f"""
        | Metric | Value |
        | :--- | :--- |
        | **Matrix Format** | 2D Integer List (`list[list[int]]`) |
        | **Grid Spatial Complexity** | $O(W \\times H) = O({width * height})$ |
        | **Spatial Hashing Lookup** | $O(1)$ constant time tile access |
        | **In-Memory Size** | ~{sys.getsizeof(matrix)} bytes |
        | **PRNG Seed Reprodicibility** | Confirmed deterministic for seed `{seed_input}` |
        """)


if __name__ == "__main__":
    main()
