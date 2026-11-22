# CodeSense AI – Video Demonstration Storyboard
**Course:** Prompt Engineering (SCSE4041) | **Milestone:** Milestone 2  
**Component:** 90–150 Second Video Demonstration (2 Marks) | **Project ID:** C4  

---

## Storyboard Overview Table

| Time Range | Scene & Frame | Visual Focus / Action | Audio Narrative Key Points | On-Screen Callouts |
|---|---|---|---|---|
| **00:00 – 00:15** | Scene 1: Title & Course Context | Camera on presenter or browser header showing CodeSense AI, SCSE4041, Project ID C4 | Introduce student, course, project title, and core problem of AI code leakage | `Course: SCSE4041`<br/>`Project ID: C4 (CodeSense AI)` |
| **00:15 – 00:35** | Scene 2: Prompt Engineering Architecture | Close-up of prompt selector and architectural diagram (P1 -> P2 -> P3) | Explain the 7 techniques: Role, Context, Task Decomposition, Few-Shot, Negative Constraints | `Role: Senior CS Instructor`<br/>`Zero Solution Leakage` |
| **00:35 – 00:65** | Scene 3: Live Buggy Code Submission | Screen recording: Load Python ZeroDivisionError example, click 'Analyze Code' | Demonstrate live input, language selection, fast execution, and Pydantic validation | `Executing Prompt P3`<br/>`RFC-8259 JSON Validation` |
| **00:65 – 00:95** | Scene 4: Socratic Results Inspection | Smooth cursor panning over Overall Assessment, High Severity, Socratic Hint Card, Positive Feedback | Highlight how hint prompts independent debugging rather than writing code | `Critical / High Severity`<br/>`Socratic Question (No Code Leaked)` |
| **00:95 – 01:20** | Scene 5: Prompt Comparison & Benchmarking | Click 'Compare P1/P2/P3' to show 3-column view; scroll down to Matplotlib chart | Contrast P1 (80% leakage) with P3 (0% leakage, 100% JSON validity) across 10 cases | `10 Test Cases Benchmarked`<br/>`P1 Leakage: 80% vs P3: 0%` |
| **01:20 – 01:35** | Scene 6: PDF Export & GitHub Wrap-Up | Click 'PDF Report' button, show generated PDF, show terminal with 26/26 tests passing | Conclude with test validation and project readiness | `26/26 Tests Passed (100%)`<br/>`Repository Prepared` |

---

## Detailed Scene Guidelines

### Scene 1: Academic Intro (15s)
- **Setting:** Full browser window displaying `http://localhost:8000/`.
- **Action:** Point cursor to top navigation bar showing `CodeSense AI`, `Milestone 2`, and `Project C4`.

### Scene 2: Prompt Design (20s)
- **Action:** Open prompt dropdown to show P1 Baseline, P2 Improved, and P3 Final Optimized.
- **Graphic:** Reference the 5-stage task decomposition pipeline displayed in the Architecture section.

### Scene 3: Live Submission & Execution (30s)
- **Action:** Select curated example `Python: Runtime Error (ZeroDivisionError)`.
- **Action:** Click `Analyze Code`. The loading spinner appears for a fraction of a second and cleanly renders results.

### Scene 4: Socratic Pedagogical Interface (30s)
- **Action:** Zoom into the **Socratic Hint Card**:
  > *"What conditional construct could you place before the division to check whether your denominator is zero?"*
- **Action:** Highlight the positive reinforcement acknowledging clean arithmetic and variable naming.

### Scene 5: Matrix Comparison & Chart (25s)
- **Action:** Click `Compare P1 / P2 / P3`.
- **Action:** Show the side-by-side columns: P1 (unstructured text revealing full fixed code), P2 (semi-structured with line hint), and P3 (pure Socratic pedagogical structure).
- **Action:** Scroll to the Phase 5 Benchmarking section showing `prompt_comparison_chart.png`.

### Scene 6: Deliverables & Test Verification (15s)
- **Action:** Click `PDF Report` and show the generated document.
- **Action:** Switch to terminal and run `pytest -v` showing 26/26 tests passed.
- **Sign-off:** Conclude with confidence.
