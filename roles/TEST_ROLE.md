# 🧪 Test Engineer Role Specification

**Role**: Test Automation & QA Engineer  
**Primary Ownership**: [`tests/*`](file:///e:/Projects/PBL/Map%20Gen/tests/TEST_ENGINEER_ROLE.md)  
**Detailed Guide**: [Test Engineer Technical Guide](file:///e:/Projects/PBL/Map%20Gen/tests/TEST_ENGINEER_ROLE.md)

---

## 🎯 Primary Responsibilities

1. **Automated Test Suite Design**: Write and maintain pytest unit and integration tests for map generators, exporters, and API routes.
2. **Seed Determinism Verification**: Assert that map generation algorithm outputs remain identical given equivalent PRNG seeds.
3. **WSGI Mock Client Scoping**: Manage Pytest fixtures (`conftest.py`) to execute mock API requests without external server processes.
4. **Binary Asset Integrity**: Verify binary HTTP payload byte headers to guarantee valid PNG image generation.

---

## 🛠 Key Tools & Technologies

- **Testing Framework**: Pytest, Pytest-Flask
- **Assertion Tools**: Deterministic matrix equality checks, binary magic byte validation
