# CodeSense AI – Demonstration Recording & Pilot Run Checklist
**Course:** Prompt Engineering (SCSE4041) | **Milestone:** Milestone 2  
**Component:** Demonstration / Pilot Run (2 Marks) & 90–150s Video (2 Marks)  

---

## 1. Pre-Recording Preparation
- [ ] **Virtual Environment Active:** `source venv/bin/activate`
- [ ] **Dependencies Installed:** `pip install fastapi uvicorn matplotlib pytest reportlab httpx pydantic`
- [ ] **FastAPI Server Running:** `uvicorn app:app --port 8000 --reload`
- [ ] **Browser Window Open:** `http://localhost:8000/` in Chrome, Safari, or Edge at 100% zoom
- [ ] **Screen Recording Software Ready:** OBS Studio, QuickTime Player (macOS), or Loom
- [ ] **Microphone Tested:** Clear audio level without background noise
- [ ] **Demo Script Accessible:** Open `demo/demo_script.md` on a secondary screen or phone

---

## 2. Live Pilot Run Sequence (Step-by-Step)

### Step 1: Initialize System
1. Open `http://localhost:8000/`
2. Verify the top badge reads `Provider: MOCK` (or `GEMINI` / `OPENAI` if you provided an API key in `.env`).
3. Notice the green shield: `Anti-Solution Leakage Enabled`.

### Step 2: Test Scenario 1 – Python Runtime Error
1. In the **"Load Curated Beginner Bug Examples"** dropdown, select:  
   `[Python] Python: Runtime Error (ZeroDivisionError)`.
2. Notice the code editor auto-populates with the code and problem description.
3. Click the gradient blue button: **"Analyze Code"**.
4. Observe the loading animation and the immediate display of results.
5. Highlight:
   - Overall Assessment
   - High Severity badge
   - Socratic Hint: *"What conditional construct could you place before the division..."*
   - Positive feedback and concept to revise.

### Step 3: Test Scenario 2 – Side-by-Side Prompt Comparison
1. Without refreshing, click the purple button: **"Compare P1 / P2 / P3"**.
2. Scroll to the **Prompt Comparison Matrix**.
3. Point out how P1 leaks the full code, whereas P3 strictly provides guided questions.

### Step 4: Test Scenario 3 – Benchmark & Metrics
1. Scroll down to **"Phase 5: Prompt Experimentation & Benchmarking"**.
2. Highlight the 10 test cases, the 0.0% leakage for P3, and the generated Matplotlib chart.

### Step 5: Test Scenario 4 – PDF Export
1. Scroll back up and click **"PDF Report"**.
2. Open the downloaded PDF in your viewer to show the faculty the formatted report.

### Step 6: Test Suite Verification
1. In your terminal, run: `pytest -v`
2. Show that all 26 tests pass with 100% success.

---

## 3. Post-Recording Validation
- [ ] Video duration is between **90 and 150 seconds** (recommended: 110–130s).
- [ ] Audio is crisp and synchronized with screen actions.
- [ ] Text in the code editor and results dashboard is easily readable at 1080p.
- [ ] The file is saved as MP4 or uploaded to YouTube/Google Drive with view permissions.
