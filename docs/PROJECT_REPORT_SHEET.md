# 🎓 Academic Project Report Sheet
**Course / Curriculum**: Problem-Based Learning (PBL)  
**Project Title**: **GenMap — Decoupled Algorithmic Procedural Map Generation Platform**  
**Evaluation Scope**: Proposal Description, System Architecture & Milestone Report (10 Pts Rubric)  
**Document Version**: 2.0.0  
**Milestone Status**: Phase 1 Shipped (Operational Prototype & Algorithmic Core)  
**Academic Year**: 2025–2026  

---

## 👥 1. Project & Team Information

### Team Overview
- **Team Name**: **Hexagon Avengers**
- **Project Title**: **GenMap** (Procedural Map Generation Platform)
- **Domain**: Procedural Content Generation (PCG), Computational Geometry, Full-Stack Web Services

### Student Roster & Engineering Role Distribution

| # | Team Member | University Roll No. | Student ID | Email Address | Academic & Technical Role |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **Manish Kanyal** *(Team Lead)* | **2519412** | **25101210025** | `mkanyal001@gmail.com` | **Project Lead & Architecture Coordinator**<br>Oversees project milestones, architectural design, team coordination, and academic compliance. |
| **2** | **Aman Singh** | **2519290** | **25101210469** | `amanyadav11633@gmail.com` | **Backend & API Systems Engineer**<br>Architects Flask REST API endpoints, CORS handling, payload validation, and in-memory byte streaming. |
| **3** | **Mehak Rawat** | **2519101** | **25103140013** | `rawatmehak456@gmail.com` | **Core Algorithm Designer**<br>Develops procedural algorithms (Cellular Automata, Moore Neighborhood voting rules, Perlin noise math). |
| **4** | **Shivansh Kala** | **2518648** | **25101281003** | `shivanshkala10@gmail.com` | **Frontend & Web Visualizer Lead**<br>Builds the HTML5 Canvas client visualizer, UI interaction sliders, responsive rendering, and client-side asset downloaders. |
| **5** | **Sagar Singh Rawat** | **2518603** | **25101280954** | `sagarrawat1517@gmail.com` | **Quality Assurance & Test Automation Lead**<br>Implements the Pytest automated testing harness, seed determinism assertions, edge-case bounds checking, and CI workflow. |
| **6** | **Priyanshu Bisht** | **2518552** | **25101280985** | `priyanshubisht285@gmail.com` | **Graphics Exporter & Documentation Specialist**<br>Engineers in-memory Pillow (PIL) rasterization pipelines, JSON matrix serialization, and technical system documentation. |

---

## 📝 2. Proposal Description (10 Points Academic Evaluation)

### 2.1 Motivation
In the domain of modern Game Development, manual level design represents a severe operational bottleneck in indie and rapid-prototype production cycles. Environment artists, level designers, and gameplay programmers dedicate a disproportionate amount of production time to manually sculpting terrain, painting tilemaps, and hand-crafting dungeon layouts cell-by-cell.

Furthermore, shipping video games with static, pre-rendered map assets dramatically inflates storage footprints (multi-megabyte binary dumps per level) and fundamentally caps replayability, as players encounter identical geometries across sessions. A purely algorithmic approach eliminates storage bloat by synthesizing complex, highly coherent worlds **deterministically in sub-5 milliseconds** from a single integer seed value. This empowers game designers to instantly prototype base level geometry, conduct spatial flow experiments, and focus their human creative energy on high-level gameplay mechanics and narrative design.

### 2.2 Current Solutions & Industry Limitations
Existing industry practices and academic alternatives suffer from three major shortcomings:

1. **Manual Level Sculpting**: Teams rely heavily on manual tile placement inside engine-specific editors (e.g., Unity Tilemap Palette, Godot GridMap, Unreal Editor). This process is slow, prone to human layout errors, and cannot adapt dynamically at runtime.
2. **Static Asset Storage Bloat**: Storing pre-baked level arrays requires disk-heavy uncompressed or compressed binary representations, spatial relational databases, or multi-megabyte image arrays per level, increasing patch sizes and initial game download footprints.
3. **Tightly-Coupled Generation Plugins**: Available procedural generation tools are almost universally locked into proprietary game engine APIs (e.g., Unity C# scripts or Godot GDScript add-ons). This tight coupling prevents reuse across lightweight web backends, headless dedicated multiplayer servers, microservices, or academic Data Structures and Algorithms (DSA) sandboxes.

---

## 🎯 3. Project Goals & Milestones

### 3.1 Project Goals
- **Engine-Agnostic Core**: Provide a standalone procedural generation core written in clean, dependency-free Python 3.10+ capable of integrating with any frontend or game engine client.
- **High-Speed Spatial Synthesis**: Achieve sub-5ms generation times for up to 4K tile grids ($64 \times 64$ to $100 \times 100$) using $O(1)$ flat 1D contiguous array indexing.
- **Deterministic Seed Reproducibility**: Guarantee 100% bitwise-identical spatial recreation from single numeric seeds across distinct operating systems and hardware platforms.
- **Multi-Archetype Generation**: Support distinct procedural archetypes including organic cavern networks (Cellular Automata), natural terrain elevation (Perlin Noise), and structured room partitioning (Binary Space Partitioning).
- **Decoupled Architecture**: Provide production-ready REST API microservices alongside a responsive, zero-dependency HTML5 Canvas web visualizer.

### 3.2 Chronological Project Milestones

```
+-----------------------------------------------------------------------------------------+
|                                 MILESTONE ROADMAP                                       |
|                                                                                         |
|  [ Milestone 1 ]       [ Milestone 2 ]       [ Milestone 3 ]       [ Milestone 4 ]      |
|  Core Algorithm Suite   Memory & Serialization Backend API & Web    Testing & Academic  |
|  • Cellular Automata    • 1D Flat Buffers     • Flask REST API      • Pytest Suite      |
|  • Perlin Noise         • Pillow In-Memory    • Canvas UI Visualizer• CI Verification   |
|  • BSP Tree Partition   • JSON Matrix Export  • Parameter Controls  • Comprehensive Docs|
+-----------------------------------------------------------------------------------------+
```

1. **Milestone 1 — Core Algorithm Suite**:
   - Implement Cellular Automata with 4-5 hysteresis voting rules and Moore Neighborhood sampling.
   - Implement smooth gradient Perlin Noise for elevation and natural biome distribution.
   - Implement Binary Space Partitioning (BSP) tree recursion for architectural dungeon rooms.
   - Validate traversability and cavity isolation using BFS flood-fill algorithms.
2. **Milestone 2 — Memory Optimization & Serialization Layer**:
   - Architect a high-speed 1D flattened row-major contiguous memory buffer ($\text{Index} = y \times W + x$) to optimize CPU L1/L2 cache locality.
   - Build an in-memory Pillow (PIL) rasterization pipeline streaming clean PNG byte streams (`image/png`) via `io.BytesIO` without temporary disk I/O.
   - Construct a structured JSON tilemap matrix serialization engine containing dimensional and density metadata.
3. **Milestone 3 — Backend REST API & Web Visualizer**:
   - Deploy Flask REST API endpoints (`/api/generate`, `/api/export`, `/health`) with robust error handling and Cross-Origin Resource Sharing (CORS).
   - Develop an interactive, zero-dependency HTML5 Canvas web client featuring dynamic tile scaling, dark-mode aesthetics, and real-time parameter tweaking.
4. **Milestone 4 — Testing, Verification & Academic Documentation**:
   - Achieve 100% test coverage for PRNG seed determinism, boundary validation, and image headers using Pytest.
   - Establish GitHub Actions CI pipeline for continuous cross-platform verification.
   - Publish complete technical specifications, role documentation, and academic evaluation reports.

---

## 🏗️ 4. Project Approach & Three-Tier Architecture

GenMap employs a decoupled, three-tier architecture that cleanly separates mathematical procedural synthesis, web service orchestration, and visual presentation:

```
[ 1. Frontend / UI ]
  • Web Canvas UI (HTML5 / Vanilla JavaScript)
  • Game Engine Clients (Godot / Unity / Pygame)
          │
          │  HTTP / JSON Requests
          ▼
[ 2. Backend / API ]
  • Flask REST API Microservice
  • Pillow (PIL) In-Memory PNG & JSON Exporters
          │
          │  Direct In-Memory Method Calls
          ▼
[ 3. Core Engine ]
  • Algorithms: Cellular Automata | Perlin Noise | BSP Trees
  • Fast 1D Array Memory Buffers (NumPy / Native Contiguous Buffers)
```

### Tier Technical Breakdown
1. **Tier 1 — Frontend & Visualizer (`frontend/`, `web/`)**:
   - Built with modern HTML5 Canvas, responsive CSS3, and lightweight Vanilla JavaScript.
   - Renders procedural grids in real-time with pixel-crisp scaling, live metric dashboards (wall density %, floor area), and one-click asset downloads.
   - Can easily be swapped with game engine clients (Godot GDScript, Unity C#, Pygame) consuming raw JSON or PNG payloads over HTTP.
2. **Tier 2 — Backend Service Layer (`backend/`)**:
   - Powered by a lightweight Python Flask microservice using the Factory and Strategy Object-Oriented design patterns.
   - Routes incoming generation parameters (`seed`, `width`, `height`, `fill_probability`, `smoothing_steps`).
   - Uses Pillow (PIL) and `io.BytesIO` to encode color-mapped PNG graphics on the fly directly in RAM, preventing disk thrashing.
3. **Tier 3 — Algorithmic Core Engine (`backend/algorithms/`)**:
   - Pure, engine-agnostic Python 3.10+ and NumPy implementation.
   - Maps 2D spatial coordinates into a 1D flattened contiguous array buffer:
     $$\text{Index} = y \times \text{Width} + x$$
   - Maximizes CPU cache line efficiency, eliminates pointer-chasing overhead common in nested lists, and guarantees deterministic execution across platforms.

---

## ⚙️ 5. System Architecture & Component Data Flow

The diagram below details the end-to-end data lifecycle from user input to rendered output:

```
[ Client / Browser ]
        │
        │  1. POST /api/generate { seed: 42, width: 40, height: 40, ... }
        ▼
[ Flask REST API Controller ]
  • Validates parameter bounds & data types
  • Selects algorithmic generator strategy (Cellular Automata / Perlin / BSP)
        │
        │  2. Execute generation with configured PRNG seed
        ▼
[ Procedural Generation Core ]
  • Pseudo-Random Initial Grid Seeding
  • Iterative Smoothing Passes (4-5 Moore Neighborhood Rule)
  • Boundary Enforcement & Cave Wall Synthesis
        │
        │  3. Raw 1D Flattened Integer Array Buffer [Index = y * W + x]
        ▼
[ Memory & Serialization Engine ]
  • Pillow (PIL) Color Rasterizer  --->  In-Memory Binary PNG Stream (BytesIO)
  • Matrix Formatter                --->  JSON Structured Payload
        │
        │  4. HTTP 200 OK (JSON Matrix or Raw image/png Binary Stream)
        ▼
[ Client Response & Canvas Display ]
  • HTML5 Canvas dynamic grid rendering
  • Live metrics calculation (floor count, wall %, processing time)
  • Asset download button trigger (.png / .json)
```

---

## 📦 6. Project Outcomes & Deliverables

1. **Modular Procedural Algorithm Library**:
   - Engine-agnostic Python package implementing Cellular Automata cave generation, Perlin noise gradient maps, and Binary Space Partitioning dungeon layouts.
2. **Production-Ready REST API Server**:
   - High-throughput Flask server featuring endpoints:
     - `GET /health` — Service health and readiness verification.
     - `POST /api/generate` — Parameterized grid synthesis returning JSON matrices.
     - `POST /api/export` — On-the-fly streaming of high-resolution PNG image assets.
3. **Interactive Web Visualizer**:
   - Responsive, dependency-free web playground allowing game designers to visually interact with algorithms, adjust seeds, toggle dimensions ($5\times5$ to $100\times100$), and inspect metrics in real time.
4. **Automated Test Suite & Verification Harness**:
   - Comprehensive Pytest test harness validating 100% seed determinism, matrix dimension accuracy, PNG magic header byte integrity (`\x89PNG\r\n\x1a\n`), and HTTP error boundaries.
5. **Academic & Technical Documentation**:
   - Comprehensive system architecture documentation, developer setup guides, role ownership manuals for all engineering positions, and formal PBL report sheets.

---

## 🔬 7. Assumptions & Technical Constraints

- **Execution Environment**: Target host execution environment runs Python 3.10+ with standard IEEE-754 compliant floating-point arithmetic.
- **Deterministic Hashing**: Bitwise pseudo-random number generation and spatial hashing operations maintain identical 32-bit integer overflow behavior across target platforms (Windows, Linux, macOS).
- **In-Memory Synthesis Limits**: Generated 2D grid matrices fit entirely within standard host RAM during synthesis without requiring secondary virtual swap space.
- **Client Rendering Compatibility**: Web clients operate modern, standards-compliant browsers supporting the HTML5 Canvas 2D Rendering Context without mandatory WebGL hardware acceleration.
- **Statelessness**: REST API endpoints are completely stateless; each request is self-contained with its own seed and configuration parameters.

---

## 📊 8. Feature Delivery Status & Implementation Matrix

| Capability Category | Specific Feature / Subsystem | Current Status | Milestone Phase | Verification Status |
| :--- | :--- | :---: | :---: | :---: |
| **Procedural Core** | Cellular Automata Cave Synthesis (4-5 Rule) | **Shipped** | Milestone 1 | ✅ Verified (Pytest) |
| **Procedural Core** | Deterministic PRNG Seeding | **Shipped** | Milestone 1 | ✅ Verified (Pytest) |
| **Procedural Core** | Perlin Noise & Terrain Visualizer | **Shipped** | Milestone 1 | ✅ Verified (Interactive Lab) |
| **Procedural Core** | Binary Space Partitioning (BSP) Dungeons | **Shipped** | Milestone 1 | ✅ Verified (Interactive Lab) |
| **Procedural Core** | Guaranteed Path Connectivity (A* / Flood Fill) | **In Progress** | Milestone 2 | ⏳ Scheduled |
| **Backend API** | Flask REST API Service (`/api/generate`) | **Shipped** | Milestone 2 | ✅ Verified (HTTP 200) |
| **Backend API** | In-Memory Pillow PNG Streamer (`/api/export`) | **Shipped** | Milestone 2 | ✅ Verified (`io.BytesIO`) |
| **Backend API** | JSON Matrix Data Serializer | **Shipped** | Milestone 2 | ✅ Verified (JSON Schema) |
| **Frontend UI** | Responsive HTML5 Canvas Viewport | **Shipped** | Milestone 3 | ✅ Verified (Browser Tested) |
| **Frontend UI** | Dynamic Dimension & Parameter Sliders | **Shipped** | Milestone 3 | ✅ Verified (Interactive UI) |
| **Frontend UI** | Real-Time Metrics (Wall %, Floor Count) | **Shipped** | Milestone 3 | ✅ Verified (Live DOM) |
| **Frontend UI** | Instant One-Click PNG Export Button | **Shipped** | Milestone 3 | ✅ Verified (Blob Download) |
| **Quality Assurance** | Automated Pytest Suite (Unit + Integration) | **Shipped** | Milestone 4 | ✅ 10/10 Tests Passing |
| **System Docs** | Modular Role Ownership & Setup Guides | **Shipped** | Milestone 4 | ✅ Complete Markdown Docs |

---

## 📚 9. Academic References

1. **Perlin, K.** (2002). *Improving Noise*. ACM Transactions on Graphics (TOG), 21(3), 681–686.
2. **Johnson, L., Yannakakis, G. N., & Togelius, J.** (2010). *Cellular automata for real-time generation of planar and non-planar video game levels*. IEEE Transactions on Computational Intelligence and AI in Games, 2(3), 189–201.
3. **Fuchs, H., Kedem, Z. M., & Naylor, B. F.** (1980). *On visible surface generation by a priori tree structures (BSP Trees)*. ACM SIGGRAPH Computer Graphics, 14(3), 124–133.
4. **Amato, G.** (2018). *Procedural Dungeon Generation with Binary Space Partitioning*. Game Developer Resources.
5. **NumPy Developers** (2024). *NumPy Array Memory Layout and Indexing Mechanics Documentation*. Available online: [https://numpy.org/doc/](https://numpy.org/doc/)

---

## ✍️ 10. Academic Evaluation & Sign-off Sheet (10 Points Rubric)

### Evaluation Rubric

| Criteria | Maximum Points | Awarded Points | Evaluator Remarks |
| :--- | :---: | :---: | :--- |
| **Problem Formulation & Motivation**<br>*Clarity of problem, industry bottlenecks, and necessity of PCG* | 2.0 | | |
| **Algorithmic Design & Mathematical Rigor**<br>*Cellular Automata, Perlin noise, BSP partitioning, flat 1D array math* | 2.5 | | |
| **System Architecture & Implementation**<br>*Decoupled 3-tier model, Flask REST API, Pillow in-memory streaming, Canvas UI* | 2.5 | | |
| **Testing, Validation & Determinism**<br>*Pytest coverage, seed determinism assertions, edge-case bounds handling* | 1.5 | | |
| **Documentation, Deliverables & Presentation**<br>*Code clarity, API specifications, live interactive demonstration* | 1.5 | | |
| **TOTAL SCORE** | **10.0** | | |

### Review & Sign-off Status

| Role | Name | Date | Signature / Status |
| :--- | :--- | :---: | :---: |
| **Team Lead (Student Representative)** | **Manish Kanyal** | September 5, 2026 | *Submitted for Evaluation* |
| **Technical QA Lead** | **Sagar Singh Rawat** | September 5, 2026 | *Verified & Tests Passing* |
| **PBL Course Evaluator / Faculty Guide** | ____________________________________ | _____ / _____ / 2026 | [ ] Approved &bull; [ ] Revisions Required |
