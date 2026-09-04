# 🎨 Frontend Module — Interactive Canvas UI

Welcome to the **Frontend** directory! This directory houses the primary client-side web application for MapGen Engine. It communicates with the Python Flask API to render high-performance HTML5 Canvas maps.

---

## 🧒 Explain Like I'm 5 (ELI5)

> Think of this frontend like a **TV screen connected to your game console**:
>
> 1. You press buttons on your controller (the input boxes for **Seed**, **Width**, and **Height**).
> 2. You tap the big **"⚡ Generate Map"** button.
> 3. The frontend sends a message over the internet wire to the Python Backend asking for a map matrix.
> 4. Once the backend sends the matrix back, your TV screen (HTML5 Canvas) instantly paints dark wall blocks and bright floor paths!
> 5. You can tap **"⬇ Download PNG"** to save your map picture directly to your computer!

---

## ⚙️ How It Works & Methodology

The frontend application uses vanilla JavaScript, modern CSS glassmorphism styling, and HTML5 Canvas API:

- **Asynchronous Fetch Requests (`fetch API`)**:
  - `POST /api/generate`: Sends `{ seed, width, height }` as JSON to the Flask server.
  - `POST /api/export`: Downloads the PNG image directly as a BLOB and triggers a browser download.
- **Dynamic HTML5 Canvas Rendering**:
  - `app.js` calculates optimal tile sizes based on grid dimensions.
  - Draws wall cells (`1`) in dark purple/gray (`#1e1e2e`) and floor cells (`#89b4fa`) with subtle grid borders.
- **Responsive State Management**:
  - Displays loading spinners on buttons during network fetch calls.
  - Shows friendly error messages in the status bar if the backend server is offline or returns invalid input error codes (400/500).

---

## 📂 Files in This Directory

| File | Type | Description |
| :--- | :--- | :--- |
| 📄 [`index.html`](file:///e:/Projects/PBL/Map%20Gen/frontend/index.html) | Markup | Main web page structure with input controls, glassmorphic container, and HTML5 Canvas element. |
| 📄 [`app.js`](file:///e:/Projects/PBL/Map%20Gen/frontend/app.js) | JavaScript | Event handling, API communication, canvas drawing logic, and PNG download triggers. |
| 📄 [`style.css`](file:///e:/Projects/PBL/Map%20Gen/frontend/style.css) | Stylesheet | Vanilla CSS featuring vibrant gradients, glassmorphism card styling, responsive layouts, and glow effects. |

---

## 🎮 How to Run

1. Make sure the backend Flask API is running (`python backend/app.py` on port `5000`).
2. Open [`index.html`](file:///e:/Projects/PBL/Map%20Gen/frontend/index.html) directly in any web browser!
3. Enter seed values (e.g. `42`, `100`, `999`), set width and height, and click **Generate Map**.
