# CodeSense AI – Milestone 2 Submission Audit & Evaluation Checklist
**Course:** Prompt Engineering (SCSE4041)  
**Milestone:** Milestone 2 – Prompt Design, Experimentation, Implementation & Demonstration  
**Total Marks:** 12  
**Project ID:** C4 | **Project Title:** Code Review Assistant for Beginner Programmers  
**Working Project Name:** CodeSense AI  
**Audit Timestamp:** November 02, 2026  

---

## Executive Audit Summary

Every deliverable required by the Milestone 2 rubric has been implemented, validated, and documented. This checklist provides an itemized mapping of all 12 marks to concrete files and evidence.

---

## 1. Itemized Component Audit (Mapped to 12 Marks)

### Component 1: Prompt / Solution Design (2 Marks)
- **Required Deliverable:**
  - Dedicated prompt engineering architecture implementing role prompting, context prompting, constraint-based prompting, task decomposition, few-shot prompting, structured output prompting, and iterative refinement.
  - Separate storage and execution of three prompt versions (P1 Baseline, P2 Improved, P3 Final Optimized).
  - Explicit anti-leakage constraints preventing full code solutions.
  - Dedicated Prompt Design Document (`.md` and `.pdf`).
- **File Locations:**
  - `prompts/baseline_prompt.txt`
  - `prompts/improved_prompt.txt`
  - `prompts/final_prompt.txt`
  - `backend/prompt_manager.py`
  - `docs/prompt_design_document.md`
  - `docs/prompt_design_document.pdf`
- **Completion Status:** **Completed and Verified**
- **Evidence Available:**
  - All 3 prompt files exist and are verified by unit tests (`tests/test_prompt_manager.py`).
  - P3 contains 5-stage task decomposition, 3 few-shot exemplars (Python, C++, Java), and explicit zero-leakage negative constraints.
  - `docs/prompt_design_document.pdf` generated with ReportLab.
- **Remaining Work:** None.

---

### Component 2: Running / Partial Build / Implementation (3 Marks)
- **Required Deliverable:**
  - Fully functional application with modern frontend and backend.
  - Interactive web dashboard with syntax highlighting, language selector (C++, Python, Java), prompt selector, loading state, error notifications, and history.
  - Robust backend with request sanitization, response parsing, JSON schema validation, timeout handling, and multi-provider LLM support (Gemini, OpenAI, Mock).
  - Downloadable PDF and Markdown review reports.
  - Zero host code execution guardrails.
- **File Locations:**
  - `app.py`
  - `backend/config.py`
  - `backend/llm_client.py`
  - `backend/prompt_manager.py`
  - `backend/response_parser.py`
  - `backend/validator.py`
  - `backend/report_generator.py`
  - `frontend/index.html`
  - `frontend/static/css/style.css`
  - `frontend/static/js/app.js`
  - `frontend/static/js/examples.js`
- **Completion Status:** **Completed and Verified**
- **Evidence Available:**
  - Web dashboard operational at `http://localhost:8000/`.
  - All 26 automated unit/integration tests passing (100% pass rate in `pytest`).
  - PDF generation verified producing valid binary PDF streams.
- **Remaining Work:** None.

---

### Component 3: Demonstration / Pilot Run (2 Marks)
- **Required Deliverable:**
  - Live pilot demonstration capability.
  - At least 5 clearly documented demonstration scenarios covering syntax errors, runtime crashes, off-by-one errors, recursion limits, and clean code.
  - Step-by-step pilot run guide and verification instructions.
- **File Locations:**
  - `demo/test_scenarios.md`
  - `demo/demonstration_checklist.md`
  - `docs/testing_report.md` (Section 3: Live Demonstration Scenarios)
- **Completion Status:** **Completed and Verified**
- **Evidence Available:**
  - 5 test scenarios fully documented with input code, expected findings, actual CodeSense AI output, and pass/fail status.
  - Curated examples dropdown embedded directly into the frontend for instantaneous 1-click pilot execution.
- **Remaining Work:** None.

---

### Component 4: Updated Git Repository (2 Marks)
- **Required Deliverable:**
  - Professionally structured repository with clean directory hierarchy.
  - Production-ready `README.md` containing problem statement, architecture, installation, experiment results, and screenshots.
  - Configuration files: `.env.example`, `.gitignore`, `requirements.txt`.
  - Git repository initialization and commit history prepared for push.
- **File Locations:**
  - `README.md`
  - `requirements.txt`
  - `.env.example`
  - `.gitignore`
  - `.git/`
- **Completion Status:** **Completed and Verified**
- **Evidence Available:**
  - Clean repository structure confirmed by file system inspection.
  - Git repository initialized with `.gitignore` properly excluding virtual environments and credentials.
- **Remaining Work:** User to add remote GitHub repository URL and push when ready.

---

### Component 5: Technical Report / Synopsis (1 Mark)
- **Required Deliverable:**
  - Comprehensive 21-section academic technical report covering title page, abstract, problem statement, objectives, existing solutions, methodology, system architecture, experimentation, testing, screenshots, limitations, future scope, and references.
  - Credible, working academic and industry citations with URLs.
  - Compiled PDF version of the report (`technical_report.pdf`).
- **File Locations:**
  - `docs/technical_report.md`
  - `docs/technical_report.pdf`
  - `docs/diagrams/01_overall_system_architecture.mmd`
  - `docs/diagrams/02_prompt_engineering_workflow.mmd`
  - `docs/diagrams/03_input_to_output_dataflow.mmd`
  - `docs/diagrams/04_application_component_architecture.mmd`
  - `docs/diagrams/05_prompt_experimentation_workflow.mmd`
- **Completion Status:** **Completed and Verified**
- **Evidence Available:**
  - All 21 sections fully written without placeholder text.
  - Real citations included (NeurIPS, SIGCSE, ACM, Google AI).
  - Formatted PDF (`docs/technical_report.pdf`, 20 KB) built and verified.
- **Remaining Work:** None.

---

### Component 6: 90–150 Second Video Demonstration Package (2 Marks)
- **Required Deliverable:**
  - Exact timed spoken script matching the 90–150 second evaluation window.
  - Frame-by-frame visual storyboard with timestamped audio and visual cues.
  - Recording checklist and instructions.
  - Genuine application visual assets in `screenshots/`.
- **File Locations:**
  - `demo/demo_script.md` (Timed at 125 seconds)
  - `demo/video_storyboard.md` (6 scenes mapped 00:00 to 01:35)
  - `demo/demonstration_checklist.md`
  - `screenshots/01_prompt_comparison_chart.png`
  - `screenshots/02_dashboard_interface.png`
- **Completion Status:** **Implemented & Ready for User Recording**
- **Evidence Available:**
  - Complete timed word-for-word spoken script.
  - Scene-by-scene storyboard with on-screen visual callouts.
  - Recording checklist ready for user recording with OBS/QuickTime/Loom.
- **Remaining Work:** Pending User Action: Record the video using the provided script and storyboard, then submit the MP4 or unlisted video link.

---

## 2. Summary Status Table

| Evaluation Component | Marks | Deliverable Artifacts | Status |
|---|:---:|---|:---:|
| **Prompt / Solution Design** | 2 | `prompts/*.txt`, `docs/prompt_design_document.md/.pdf` | **Completed & Verified** |
| **Running Implementation** | 3 | `app.py`, `backend/`, `frontend/`, 26 tests | **Completed & Verified** |
| **Demonstration / Pilot Run** | 2 | `demo/test_scenarios.md`, Live UI pilot | **Completed & Verified** |
| **Updated Git Repository** | 2 | `README.md`, `requirements.txt`, repo structure | **Completed & Verified** |
| **Technical Report / Synopsis** | 1 | `docs/technical_report.md/.pdf` (21 sections) | **Completed & Verified** |
| **90–150s Video Demonstration** | 2 | `demo/demo_script.md`, `demo/video_storyboard.md` | **Ready for Recording** |
| **TOTAL** | **12 / 12** | **Full Milestone 2 Submission Package** | **100% Prepared** |
