# CHANGELOG: CodeSense AI
**Course:** Prompt Engineering (SCSE4041) | **Project ID:** C4  
**Project Title:** Code Review Assistant for Beginner Programmers  

All notable changes and architectural milestones achieved since Milestone 1 submission.

---

## [Milestone 2] - 2026-11-16 (Current Submission)
### Added
- **Final Optimized Prompt (P3):** Implemented 5-stage task decomposition (Syntax -> Semantics -> Severity -> Socratic Hints -> Positive Reinforcement), multi-language few-shot exemplars (Python, C++, Java), and strict negative constraints prohibiting complete code leakage.
- **Improved Prompt (P2):** Implemented empathetic instructor persona, standardized severity taxonomy (`Critical`, `High`, `Medium`, `Low`, `No issue detected`), and basic JSON schema.
- **Baseline Prompt (P1):** Documented zero-shot naive prompt used for comparative evaluation.
- **Empirical Benchmarking Suite (`experiments/`):** Tested 10 representative beginner programs across 6 criteria; generated `experiment_results.csv` and `prompt_comparison_chart.png`.
- **FastAPI Backend (`backend/`):** Created asynchronous REST endpoints for code analysis, live 3-way prompt comparison matrix, session history, and report export.
- **Multi-Provider LLM Integration (`backend/llm_client.py`):** Added support for Google Gemini 2.5 Flash, OpenAI GPT-4o mini, and an offline deterministic Pedagogical Mock Engine for reliable demonstration.
- **Interactive Single-Page Dashboard (`frontend/`):** Built responsive web dashboard with code editor, language selector (Python, C++, Java), prompt switcher, curated beginner bug examples, and live Socratic hint rendering.
- **Report Generation (`backend/report_generator.py`):** Enabled instant one-click export to formatted PDF (via ReportLab) and Markdown.
- **Automated Test Suite (`tests/`):** Implemented 26 unit and integration tests with 100% pass rate in `pytest`.
- **Milestone 2 Compliance Documentation (`docs/`):**
  - Milestone 2 Comprehensive Submission PDF (`M2_C4_CodeSenseAI.pdf`) structured into all 7 mandatory sections.
  - Supporting Document PDF (`CodeSense_TechnicalReport.pdf`).
  - 5 System Architecture Mermaid diagrams (`docs/diagrams/`).
  - 90–150s Video demonstration script and visual storyboard (`demo/`).

### Changed
- Refined anti-leakage constraints to eliminate line-level code spoilers, moving from 80% leakage in P1 and 20% in P2 to **0% leakage in P3**.
- Enhanced JSON response parser with heuristic repair to resolve trailing commas and missing quotes.

---

## [Milestone 1] - 2026-10-15
### Added
- Initial project proposal and problem definition for Project C4 (Code Review Assistant for Beginner Programmers).
- Identified target user persona: First-year undergraduate computing students.
- Outlined theoretical requirements: Socratic questioning over code generation.
- Selected core languages: Python, C++, and Java.
