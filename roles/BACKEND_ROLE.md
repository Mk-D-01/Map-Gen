# ⚙️ Backend Engineer Role Specification

**Role**: Backend Software Engineer  
**Primary Ownership**: [`backend/app.py`](file:///e:/Projects/PBL/Map%20Gen/backend/app.py), [`backend/export/*`](file:///e:/Projects/PBL/Map%20Gen/backend/export/EXPORTER_ENGINEER_ROLE.md)  
**Detailed Guide**: [Backend Technical Guide](file:///e:/Projects/PBL/Map%20Gen/backend/BACKEND_ENGINEER_ROLE.md)

---

## 🎯 Primary Responsibilities

1. **REST API Endpoint Engineering**: Design and maintain Flask REST endpoints (`/health`, `/api/generate`, `/api/export`).
2. **Dynamic Dependency Injection**: Maintain `MapGenApp` to dynamically inject grid generator and image exporter dependencies.
3. **In-Memory Streaming**: Optimize image export routes to render PNG buffers directly in RAM (`io.BytesIO`) without temporary disk files.
4. **CORS & Middleware Security**: Manage CORS policy settings to ensure seamless communication with frontend web clients.

---

## 🛠 Key Tools & Technologies

- **Language & Framework**: Python 3.9+, Flask, Flask-CORS
- **Image Processing**: Pillow (PIL)
- **Data Transfer**: JSON, BytesIO binary streams
- **Testing**: pytest, pytest-flask
