# 🎨 Frontend Engineer Role Guide — Interactive Canvas Application

**Role**: Frontend Web Engineer  
**Scope**: HTML5 Canvas Rendering, DOM Event Controller, Asynchronous Fetch API, BLOB Image Downloading  
**Primary Directory**: [`frontend/`](file:///e:/Projects/PBL/Map%20Gen/frontend/FRONTEND_ENGINEER_ROLE.md)

---

## 🔬 How It Works Under the Hood

The frontend client is built with HTML5, Vanilla JavaScript, and CSS Glassmorphism styling. It communicates asynchronously with the Flask backend API to display and download procedural maps.

```
 User Inputs                   app.js Controller                   Render Target
+--------------+              +-------------------+               +----------------+
| Seed: 42     | -----------> | Asynchronous      | ------------> | HTML5 Canvas   |
| Width/Height |              | fetch() API Call  |               | 2D Context     |
+--------------+              +-------------------+               +----------------+
                                        |
                                        v
                              +-------------------+
                              | BLOB Image        | ------------> Download PNG
                              | Download Link     |
                              +-------------------+
```

### 1. Client Controller Workflow (`app.js`)
- Located in [`app.js`](file:///e:/Projects/PBL/Map%20Gen/frontend/app.js).
- **User Event Handling**: Captures click events on the **Generate Map** and **Download PNG** buttons.
- **API Fetch Communication**: Sends asynchronous `POST` requests containing `{ seed, width, height }` as JSON to `http://127.0.0.1:5000/api/generate`.

### 2. HTML5 Canvas Rendering Engine
1. Receives the 2D matrix array from the backend API.
2. Calculates dynamic tile pixel dimensions so the map fits cleanly inside the canvas surface.
3. Clears previous drawings and iterates through every grid row and column:
   - Paints wall cells (`1`) in dark slate (`#1e1e2e`).
   - Paints floor cells (`0`) in light blue (`#89b4fa`).

### 3. Programmatic File Downloading
- When the user clicks **Download PNG**, `app.js` calls `POST /api/export`.
- Converts the returned binary byte stream into a temporary browser `Blob` object URL (`URL.createObjectURL(blob)`).
- Programmatically triggers a file download directly in the user's browser.

---

## 📂 Subsystem File Overview

| File | Purpose |
| :--- | :--- |
| 📄 [`index.html`](file:///e:/Projects/PBL/Map%20Gen/frontend/index.html) | Main web page structure containing input controls, status panels, and HTML5 Canvas. |
| 📄 [`app.js`](file:///e:/Projects/PBL/Map%20Gen/frontend/app.js) | Client JavaScript file managing API requests, canvas rendering, and downloads. |
| 📄 [`style.css`](file:///e:/Projects/PBL/Map%20Gen/frontend/style.css) | Custom CSS stylesheet with glassmorphism design, dark mode theme, and responsive layouts. |

---

## 🎮 How to Run

1. Start the Flask backend server (`python backend/app.py`).
2. Open [`index.html`](file:///e:/Projects/PBL/Map%20Gen/frontend/index.html) directly in any web browser!
