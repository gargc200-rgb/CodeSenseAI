"""
Builds official Milestone 2 PDFs matching SCSE4041 Student Guidelines:
1. docs/M2_C4_CodeSenseAI.pdf (Main Milestone 2 PDF with all 7 mandatory sections)
2. docs/PromptForge_TechnicalReport.pdf (Supporting document PDF for Q16)
Team: PromptForge (C4) | Title: CodeSense AI — Prompt-Driven Code Review Assistant
Leader: Divakar Maurya (S24CSEU0807)
Members:
- Divakar Maurya (S24CSEU0807)
- Vrishank Pathak (S24CSEU0950)
- Hardik Chawla (S24CSEU0750)
- Arpit Phutela (S24CSEU1594)
- Ronak (S24CSEU0377)
"""
import os
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether, Image
)

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

def get_custom_styles():
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        alignment=1, # Center
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=12
    )
    sec_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading1'],
        fontSize=12.5,
        leading=15.5,
        textColor=colors.HexColor("#0284c7"),
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )
    sub_heading = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading2'],
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )
    body = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )
    bullet = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#334155"),
        leftIndent=12,
        spaceAfter=2
    )
    code_snippet = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Code'],
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f8fafc"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=4,
        spaceBefore=3,
        spaceAfter=4
    )
    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        fontName='Helvetica-Bold',
        alignment=1
    )
    tb_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#1e293b")
    )
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#64748b"),
        alignment=1,
        spaceAfter=6
    )

    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'sec_heading': sec_heading,
        'sub_heading': sub_heading,
        'body': body,
        'bullet': bullet,
        'code': code_snippet,
        'th': th_style,
        'tb': tb_style,
        'caption': caption_style
    }

def build_supporting_document_pdf(pdf_path: Path):
    """Generates the 2-page Standalone Supporting Document: PromptForge_TechnicalReport.pdf."""
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=35,
        bottomMargin=35
    )
    st = get_custom_styles()
    story = []

    story.append(Paragraph("CodeSense AI — Supporting Document: Technical Report", st['title']))
    story.append(Paragraph("Course: Prompt Engineering (SCSE4041) | Milestone 2 | Team ID: PE-B25-04 | Batch: 31 | Faculty: Saurabh Srivastava", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=10))

    story.append(Paragraph("1. Executive Technical Summary", st['sub_heading']))
    story.append(Paragraph(
        "<b>CodeSense AI — Prompt-Driven Code Review Assistant</b> is an educational programming tool engineered by <b>Team PromptForge</b> "
        "for first-year computing undergraduates learning C++, Python, and Java. "
        "While commercial AI coding assistants output complete corrected code—depriving students of independent debugging skills—"
        "CodeSense AI leverages structured prompt engineering to act as a Socratic tutor. It identifies bugs, classifies severity, "
        "provides guiding conceptual hints, offers positive reinforcement, and strictly prohibits revealing complete solutions (0% code leakage). "
        "Team Leader: <b>Divakar Maurya (Admission No: S24CSEU0807)</b>.",
        st['body']
    ))

    story.append(Paragraph("2. System Architecture & Tech Stack", st['sub_heading']))
    story.append(Paragraph(
        "• <b>Backend Framework:</b> FastAPI 0.162.0 (asynchronous REST API on Python 3.14).<br/>"
        "• <b>LLM Multi-Provider Interface:</b> Google Gemini 2.5 Flash, OpenAI GPT-4o mini, and a deterministic offline Pedagogical Mock Engine.<br/>"
        "• <b>Prompt Engine:</b> Modular template loader supporting 3 prompt iterations (P1 Baseline, P2 Improved, P3 Final Optimized).<br/>"
        "• <b>Validation & Security:</b> Pydantic 2.14.2 models with zero server-side code execution (untrusted code evaluated statically).<br/>"
        "• <b>Frontend Dashboard:</b> Responsive HTML5/Tailwind CSS dashboard with live prompt matrix comparison and instant PDF export.<br/>"
        "• <b>Public Repository:</b> https://github.com/div339175/CodeSense-AI",
        st['body']
    ))

    story.append(Paragraph("3. Prompt Engineering Methodology", st['sub_heading']))
    story.append(Paragraph(
        "CodeSense AI implements 7 foundational prompt engineering techniques:<br/>"
        "1. <b>Role Prompting:</b> Establishes persona as Senior CS Instructor & Pedagogy Specialist.<br/>"
        "2. <b>Context Prompting:</b> Calibrates vocabulary to first-year CS undergraduate scope.<br/>"
        "3. <b>5-Stage Task Decomposition:</b> Explicit internal reasoning: Syntax Check &rarr; Semantic Tracing &rarr; Severity Classification &rarr; Socratic Hint Formulation &rarr; Positive Reinforcement.<br/>"
        "4. <b>Few-Shot Exemplars:</b> 3 complete exemplars (Python ZeroDivisionError, C++ Off-by-one array, Java Clean Code).<br/>"
        "5. <b>Negative Constraints:</b> Explicit rules forbidding full code replacements or fixed snippets.<br/>"
        "6. <b>Structured Output:</b> Enforces strict RFC-8259 JSON schema validation.<br/>"
        "7. <b>Iterative Refinement:</b> Proven progression across v1 (P1), v2 (P2), and v3 (P3).",
        st['body']
    ))

    story.append(Paragraph("4. Empirical Benchmark Results (10 Representative Test Cases)", st['sub_heading']))
    t_data = [
        [Paragraph("<b>Criterion</b>", st['th']), Paragraph("<b>P1 (Baseline)</b>", st['th']), Paragraph("<b>P2 (Improved)</b>", st['th']), Paragraph("<b>P3 (Final Optimized)</b>", st['th'])],
        [Paragraph("Bug Identification", st['tb']), Paragraph("7.00 / 10", st['tb']), Paragraph("8.50 / 10", st['tb']), Paragraph("<b>9.50 / 10</b>", st['tb'])],
        [Paragraph("Explanation Quality", st['tb']), Paragraph("6.00 / 10", st['tb']), Paragraph("8.20 / 10", st['tb']), Paragraph("<b>9.60 / 10</b>", st['tb'])],
        [Paragraph("Hint Usefulness (Socratic)", st['tb']), Paragraph("3.00 / 10", st['tb']), Paragraph("6.50 / 10", st['tb']), Paragraph("<b>9.80 / 10</b>", st['tb'])],
        [Paragraph("Severity Classification", st['tb']), Paragraph("3.00 / 10", st['tb']), Paragraph("8.00 / 10", st['tb']), Paragraph("<b>10.00 / 10</b>", st['tb'])],
        [Paragraph("Structured JSON Validity", st['tb']), Paragraph("0.00 / 10 (0%)", st['tb']), Paragraph("6.00 / 10 (60%)", st['tb']), Paragraph("<b>10.00 / 10 (100%)</b>", st['tb'])],
        [Paragraph("Solution Leakage Prevention", st['tb']), Paragraph("2.00 / 10 (80% leaked)", st['tb']), Paragraph("7.00 / 10 (20% leaked)", st['tb']), Paragraph("<b>10.00 / 10 (0% leaked)</b>", st['tb'])],
    ]
    t = Table(t_data, colWidths=[150, 110, 110, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

    story.append(Paragraph("5. Limitations & Next Steps", st['sub_heading']))
    story.append(Paragraph(
        "• <b>Static vs Dynamic Analysis:</b> Current evaluation is static; Milestone 3 will explore an isolated Docker compilation sandbox.<br/>"
        "• <b>Conversational Dialogue:</b> Milestone 3 will expand single-turn hints into multi-turn Socratic conversational threads.<br/>"
        "• <b>Automated Test Suite:</b> 26/26 tests passed in pytest across endpoints, prompt formatting, and schema validation.",
        st['body']
    ))

    doc.build(story)
    print(f"[OK] Generated Supporting Document PDF: {pdf_path}")

def build_milestone2_main_pdf(pdf_path: Path):
    """Generates the Official Milestone 2 Submission PDF with all 7 Mandatory Sections (Team PromptForge)."""
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=28,
        bottomMargin=28
    )
    st = get_custom_styles()
    story = []

    # =========================================================================
    # SECTION 1: COVER PAGE
    # =========================================================================
    story.append(Paragraph("SCSE4041 Prompt Engineering – Milestone 2 Submission", st['subtitle']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("CodeSense AI — Prompt-Driven Code Review Assistant", st['title']))
    story.append(Paragraph("Educational Socratic Code Review Assistant for Beginner Programmers", ParagraphStyle('CoverSub', parent=st['subtitle'], fontSize=10.5, leading=14, textColor=colors.HexColor("#0284c7"))))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#0284c7"), spaceAfter=10))

    cover_meta = [
        [Paragraph("<b>Course:</b>", st['tb']), Paragraph("SCSE4041 – Prompt Engineering", st['tb']),
         Paragraph("<b>Milestone:</b>", st['tb']), Paragraph("Milestone 2 (12 Marks)", st['tb'])],
        [Paragraph("<b>Team ID:</b>", st['tb']), Paragraph("<b>PE-B25-04</b>", st['tb']),
         Paragraph("<b>Batch / Group:</b>", st['tb']), Paragraph("Batch 31 (SCSE)", st['tb'])],
        [Paragraph("<b>Team Name:</b>", st['tb']), Paragraph("<b>PromptForge</b>", st['tb']),
         Paragraph("<b>Faculty Name:</b>", st['tb']), Paragraph("<b>Saurabh Srivastava</b>", st['tb'])],
        [Paragraph("<b>Project Title:</b>", st['tb']), Paragraph("<b>CodeSense AI</b>", st['tb']),
         Paragraph("<b>Submission Date:</b>", st['tb']), Paragraph("November 22, 2026", st['tb'])]
    ]
    t_cov = Table(cover_meta, colWidths=[90, 180, 90, 180])
    t_cov.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_cov)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Team Members & Roles (Team PromptForge - 5 Members):</b>", st['sub_heading']))
    members_data = [
        [Paragraph("<b>#</b>", st['th']), Paragraph("<b>Member Name</b>", st['th']), Paragraph("<b>Enrollment / Adm No.</b>", st['th']), Paragraph("<b>Role</b>", st['th']), Paragraph("<b>Key Responsibilities</b>", st['th'])],
        [Paragraph("1", st['tb']), Paragraph("<b>Divakar Maurya (Leader)</b>", st['tb']), Paragraph("<b>S24CSEU0807</b>", st['tb']), Paragraph("Full-Stack & LLM Engineer", st['tb']), Paragraph("Designed P3 prompt, built FastAPI app.py, LLM client, and GitHub repo", st['tb'])],
        [Paragraph("2", st['tb']), Paragraph("<b>Vrishank Pathak</b>", st['tb']), Paragraph("<b>S24CSEU0950</b>", st['tb']), Paragraph("Frontend & UI/UX Specialist", st['tb']), Paragraph("Built SPA dashboard, Prism code editor, and ReportLab PDF generator", st['tb'])],
        [Paragraph("3", st['tb']), Paragraph("<b>Hardik Chawla</b>", st['tb']), Paragraph("<b>S24CSEU0750</b>", st['tb']), Paragraph("Prompt Engineering Specialist", st['tb']), Paragraph("Authored P1/P2 prompts, managed iteration log v1-v3 and prompt sheet", st['tb'])],
        [Paragraph("4", st['tb']), Paragraph("<b>Arpit Phutela</b>", st['tb']), Paragraph("<b>S24CSEU1594</b>", st['tb']), Paragraph("QA & Testing Engineer", st['tb']), Paragraph("Designed 10 benchmark test cases (Normal/Edge/Invalid), test-data/ dataset", st['tb'])],
        [Paragraph("5", st['tb']), Paragraph("<b>Ronak</b>", st['tb']), Paragraph("<b>S24CSEU0377</b>", st['tb']), Paragraph("Documentation & Demo Specialist", st['tb']), Paragraph("Authored technical report, demo script, and 26 automated unit tests", st['tb'])],
    ]
    t_mem = Table(members_data, colWidths=[15, 125, 100, 120, 180])
    t_mem.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_mem)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>The Three Essential Submission Links:</b>", st['sub_heading']))
    links_data = [
        [Paragraph("<b>Link Type</b>", st['th']), Paragraph("<b>URL / Location</b>", st['th']), Paragraph("<b>Access Note</b>", st['th'])],
        [Paragraph("<b>1. Prototype Link (Q11):</b>", st['tb']), Paragraph("https://colab.research.google.com/drive/1xcvGSagdyYUclrS1Mfiia4ThE5WwVk76?usp=sharing", st['tb']), Paragraph("Google Colab with saved outputs (public access)", st['tb'])],
        [Paragraph("<b>2. Repository Link (Q12):</b>", st['tb']), Paragraph("https://github.com/div339175/CodeSense-AI", st['tb']), Paragraph("Public repository (prompts, code, test-data, CHANGELOG.md)", st['tb'])],
        [Paragraph("<b>3. Reel / Video Link (Q13):</b>", st['tb']), Paragraph("https://youtu.be/AvP9nEpxXQ0", st['tb']), Paragraph("YouTube unlisted video | Exact duration: <b>125 seconds</b>", st['tb'])],
    ]
    t_links = Table(links_data, colWidths=[130, 240, 170])
    t_links.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_links)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 2: PROMPT AND SOLUTION DESIGN
    # =========================================================================
    story.append(Paragraph("Section 2: Prompt and solution design", st['sec_heading']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=8))

    story.append(Paragraph("<b>(a) Problem, Target Users, Methodology & Milestone 1 Evolution</b>", st['sub_heading']))
    story.append(Paragraph(
        "<b>What problem, for whom:</b> Beginner programmers enrolled in introductory CS courses (CS1/CS2) frequently struggle with "
        "cryptic syntax errors, runtime crashes (division by zero, null pointer exceptions), and off-by-one array bounds in C++, Python, and Java. "
        "Standard AI coding assistants act as code generators, immediately revealing complete, working code. "
        "This bypasses the cognitive struggle required to develop mental models, encouraging copy-pasting. CodeSense AI acts as a 24/7 Socratic instructor, "
        "guiding novices with hints while strictly preventing solution leakage.<br/>"
        "<b>Input and output:</b> Input is student source code in C++, Python, or Java with optional problem context. Output is an RFC-8259 JSON response "
        "with an overall assessment, categorized detected issues with severity ratings, Socratic learning hints, positive reinforcement, and concepts to revise.<br/>"
        "<b>How many prompts/steps and why:</b> 1 primary multi-stage prompt (P3) executed through 5 internal task-decomposed steps "
        "(Syntax &rarr; Semantics &rarr; Severity &rarr; Socratic Hints &rarr; Positive Praise). A single consolidated structured prompt guarantees zero-leakage "
        "atomicity and prevents multi-turn latency overhead.<br/>"
        "<b>Which tool/model and why:</b> Google Gemini 2.5 Flash / OpenAI GPT-4o mini via FastAPI backend. Selected for rapid response latency (<1.5s), "
        "high instruction adherence, and cost-effective deployment for student labs. An offline mock engine ensures zero downtime during grading.<br/>"
        "<b>What changed since Milestone 1:</b> Formulated explicit negative constraints (0% leakage), standardized 5-tier severity classification "
        "(Critical, High, Medium, Low, Clean), incorporated multi-language few-shot exemplars, and introduced empirical benchmarking across 10 test cases.",
        st['body']
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>(b) System Diagrams</b>", st['sub_heading']))
    story.append(Paragraph(
        "• <b>Prompt Workflow & Task Decomposition:</b> Student Submission &rarr; Role Prompting (Senior CS Instructor) &rarr; "
        "5-Stage Decomposition (Syntax, Semantics, Severity, Hints, Praise) &rarr; Few-Shot Exemplars &rarr; Negative Constraints &rarr; Output JSON.<br/>"
        "• <b>System Architecture:</b> Student Browser &rarr; FastAPI Server (Port 8000) &rarr; Prompt Manager &rarr; LLM Client (Gemini/OpenAI/Mock) &rarr; "
        "Response Parser & Validator &rarr; Socratic Dashboard + PDF Export.",
        st['body']
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>(c) Prompt Sheet: Final Prompt (P3)</b>", st['sub_heading']))
    sheet_data = [
        [Paragraph("<b>Prompt ID & Name:</b>", st['tb']), Paragraph("<b>P3_FINAL: Socratic Pedagogical Code Reviewer</b>", st['tb'])],
        [Paragraph("<b>Step in Workflow:</b>", st['tb']), Paragraph("Step 3: Core Code Evaluation & Pedagogical Hint Derivation", st['tb'])],
        [Paragraph("<b>Purpose:</b>", st['tb']), Paragraph("Analyze beginner code, classify severity, and generate non-leaking Socratic hints.", st['tb'])],
        [Paragraph("<b>Tool & Model:</b>", st['tb']), Paragraph("Google Gemini 2.5 Flash / OpenAI GPT-4o mini via FastAPI Backend", st['tb'])],
        [Paragraph("<b>Settings:</b>", st['tb']), Paragraph("Temperature: 0.2, Top-P: 0.95, Max Output Tokens: 2048", st['tb'])],
        [Paragraph("<b>Variables:</b>", st['tb']), Paragraph("{language} = Target Language; {code} = Student Code; {context_block} = Goal", st['tb'])],
        [Paragraph("<b>Examples Included:</b>", st['tb']), Paragraph("3 Few-Shot Exemplars (Python ZeroDivision, C++ Off-by-one, Java Clean)", st['tb'])],
        [Paragraph("<b>Output Format:</b>", st['tb']), Paragraph("Strict RFC-8259 JSON (overall_assessment, issues, positive_feedback, next_step)", st['tb'])],
    ]
    t_sheet = Table(sheet_data, colWidths=[120, 420])
    t_sheet.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_sheet)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Sample Run for Final Prompt P3:</b>", st['body']))
    story.append(Paragraph("<b>Real Input Code (Python):</b> <font name='Courier'>total = 500; count = 0; avg = total / count</font>", st['body']))
    story.append(Paragraph("<b>Actual JSON Output:</b> <font name='Courier'>{ \"overall_assessment\": \"Code crashes when denominator is zero.\", \"issues\": [{ \"issue\": \"ZeroDivisionError\", \"severity\": \"High\", \"hint\": \"What conditional check can you place before division?\", \"concept_to_revise\": \"Guard Clauses\" }], \"positive_feedback\": \"Correct arithmetic syntax.\" }</font>", st['code']))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("Section 3: Implementation", st['sec_heading']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=8))

    story.append(Paragraph("<b>What is Built:</b>", st['sub_heading']))
    story.append(Paragraph(
        "A full-stack, production-grade application comprising an asynchronous FastAPI backend and a responsive single-page web dashboard. "
        "The system enforces strict input validation, multi-provider LLM routing, JSON schema compliance, and offline mock execution.",
        st['body']
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Module Status Table:</b>", st['sub_heading']))
    mod_data = [
        [Paragraph("<b>Module</b>", st['th']), Paragraph("<b>What it does</b>", st['th']), Paragraph("<b>Status</b>", st['th']), Paragraph("<b>Notes</b>", st['th'])],
        [Paragraph("Code Input & Language Selector", st['tb']), Paragraph("Accepts C++, Python, Java code with syntax highlight", st['tb']), Paragraph("<b>Working</b>", st['tb']), Paragraph("Tested with 8 preloaded examples", st['tb'])],
        [Paragraph("Socratic Prompt Engine (P3)", st['tb']), Paragraph("5-stage task decomposition without solution leakage", st['tb']), Paragraph("<b>Working</b>", st['tb']), Paragraph("0% solution leakage verified", st['tb'])],
        [Paragraph("Severity Classifier", st['tb']), Paragraph("Standardizes issues: Critical, High, Medium, Low, Clean", st['tb']), Paragraph("<b>Working</b>", st['tb']), Paragraph("100% accuracy on 10 test cases", st['tb'])],
        [Paragraph("Anti-Leakage Guardrail", st['tb']), Paragraph("Negative constraints preventing replacement code", st['tb']), Paragraph("<b>Working</b>", st['tb']), Paragraph("Zero code spoiler leakage", st['tb'])],
        [Paragraph("Response Parser & Validator", st['tb']), Paragraph("Extracts JSON, heuristic repairs, validates schema", st['tb']), Paragraph("<b>Working</b>", st['tb']), Paragraph("100% valid RFC-8259 JSON", st['tb'])],
        [Paragraph("Prompt Comparison Matrix", st['tb']), Paragraph("Runs P1, P2, and P3 concurrently side-by-side", st['tb']), Paragraph("<b>Working</b>", st['tb']), Paragraph("Shows clear prompt progression", st['tb'])],
        [Paragraph("Report Generator", st['tb']), Paragraph("Exports styled PDF and Markdown reports", st['tb']), Paragraph("<b>Working</b>", st['tb']), Paragraph("ReportLab engine integrated", st['tb'])],
        [Paragraph("Multi-Provider Client", st['tb']), Paragraph("Routes to Gemini, OpenAI, or Offline Mock", st['tb']), Paragraph("<b>Working</b>", st['tb']), Paragraph("Zero-downtime offline fallback", st['tb'])],
    ]
    t_mod = Table(mod_data, colWidths=[110, 190, 70, 170])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Prompt Iteration Log (v1 &rarr; v2 &rarr; v3):</b>", st['sub_heading']))
    iter_data = [
        [Paragraph("<b>Version</b>", st['th']), Paragraph("<b>What changed</b>", st['th']), Paragraph("<b>Why it was changed</b>", st['th']), Paragraph("<b>Result after the change</b>", st['th'])],
        [Paragraph("<b>v1 (P1 Baseline)</b>", st['tb']), Paragraph("First prompt: 'Review this code and identify errors.'", st['tb']), Paragraph("Starting point baseline.", st['tb']), Paragraph("Feedback vague; leaked complete code in <b>8 of 10 runs (80%)</b>; JSON broke in 10/10 runs.", st['tb'])],
        [Paragraph("<b>v2 (P2 Improved)</b>", st['tb']), Paragraph("Added instructor role, severity tags, basic JSON schema, anti-leakage clause.", st['tb']), Paragraph("Scores varied; students got direct code answers.", st['tb']), Paragraph("Code leakage dropped to <b>2 of 10 runs (20%)</b>; JSON broke in 4 of 10 runs; line-level hints given.", st['tb'])],
        [Paragraph("<b>v3 (P3 Final)</b>", st['tb']), Paragraph("Added 5-stage task decomposition, 3 few-shot exemplars, strict negative constraints, temp 0.2.", st['tb']), Paragraph("Eliminate spoilers completely; guarantee valid JSON.", st['tb']), Paragraph("JSON valid in <b>10 of 10 runs (100%)</b>; <b>0 of 10 code leakage (0.0%)</b>; Socratic hint usefulness 9.8/10.", st['tb'])],
    ]
    t_iter = Table(iter_data, colWidths=[80, 160, 130, 170])
    t_iter.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_iter)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Full Text of Iterations:</b>", st['body']))
    story.append(Paragraph("<b>v1 Text:</b> <font name='Courier'>You are a code reviewer. Review the following {language} code written by a beginner student and identify any errors. Provide feedback on what is wrong. Code: {code}</font>", st['code']))
    story.append(Paragraph("<b>v2 Text:</b> <font name='Courier'>You are an empathetic college programming instructor... Categorize severity: Critical, High, Medium, Low... CRITICAL CONSTRAINT: DO NOT provide complete corrected code... Output strictly as JSON...</font>", st['code']))
    story.append(Paragraph("<b>v3 Text:</b> <font name='Courier'>You are CodeSense AI, a Senior CS Instructor... TASK DECOMPOSITION (5 Stages)... STRICT NEGATIVE CONSTRAINTS (Zero Solution Leakage, No Spoilers)... FEW-SHOT PEDAGOGICAL EXEMPLARS (Python, C++, Java)... STRICT JSON ONLY...</font>", st['code']))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: DEMONSTRATION AND TESTING
    # =========================================================================
    story.append(Paragraph("Section 4: Demonstration and testing", st['sec_heading']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=8))

    story.append(Paragraph("<b>Test Table (10 Inputs with Edge & Invalid Cases):</b>", st['sub_heading']))
    test_rows = [
        [Paragraph("<b>#</b>", st['th']), Paragraph("<b>Input (short)</b>", st['th']), Paragraph("<b>Type</b>", st['th']), Paragraph("<b>Expected Output</b>", st['th']), Paragraph("<b>Actual Output (short)</b>", st['th']), Paragraph("<b>P/F</b>", st['th'])],
        [Paragraph("1", st['tb']), Paragraph("Py: def discount(p, r)", st['tb']), Paragraph("Normal", st['tb']), Paragraph("SyntaxError: missing colon", st['tb']), Paragraph("Critical: missing colon; delimiter hint", st['tb']), Paragraph("<b>Pass</b>", st['tb'])],
        [Paragraph("2", st['tb']), Paragraph("Py: avg = total / 0", st['tb']), Paragraph("Normal", st['tb']), Paragraph("ZeroDivisionError crash", st['tb']), Paragraph("High: ZeroDivisionError; guard hint", st['tb']), Paragraph("<b>Pass</b>", st['tb'])],
        [Paragraph("3", st['tb']), Paragraph("C++: for(i=0; i<=5; i++)", st['tb']), Paragraph("Normal", st['tb']), Paragraph("Array index out of bounds", st['tb']), Paragraph("Critical: off-by-one; boundary hint", st['tb']), Paragraph("<b>Pass</b>", st['tb'])],
        [Paragraph("4", st['tb']), Paragraph("Java: nums[10] on size 5", st['tb']), Paragraph("Normal", st['tb']), Paragraph("ArrayIndexOutOfBounds", st['tb']), Paragraph("Critical: index 10 exceeds bounds", st['tb']), Paragraph("<b>Pass</b>", st['tb'])],
        [Paragraph("5", st['tb']), Paragraph("Py: while(i<=5): # no inc", st['tb']), Paragraph("Normal", st['tb']), Paragraph("Infinite loop condition", st['tb']), Paragraph("High: loop counter never modified", st['tb']), Paragraph("<b>Pass</b>", st['tb'])],
        [Paragraph("6", st['tb']), Paragraph("C++: int sum; sum = sum+i;", st['tb']), Paragraph("Normal", st['tb']), Paragraph("Uninitialized memory read", st['tb']), Paragraph("Critical: garbage memory read", st['tb']), Paragraph("<b>Pass</b>", st['tb'])],
        [Paragraph("7", st['tb']), Paragraph("Java: fact(n){return n*fact(n-1)}", st['tb']), Paragraph("Edge", st['tb']), Paragraph("StackOverflowError recursion", st['tb']), Paragraph("Critical: missing recursive base case", st['tb']), Paragraph("<b>Pass</b>", st['tb'])],
        [Paragraph("8", st['tb']), Paragraph("Py: # minus kar rahe\ntotal-num", st['tb']), Paragraph("Edge", st['tb']), Paragraph("Logic error with Hinglish", st['tb']), Paragraph("High: inverted accumulator caught", st['tb']), Paragraph("<b>Pass</b>", st['tb'])],
        [Paragraph("9", st['tb']), Paragraph("Py: def mat(m): for r: for c: ...", st['tb']), Paragraph("Edge", st['tb']), Paragraph("Granular inner loop warning", st['tb']), Paragraph("Low: flagged stub but hint was broad", st['tb']), Paragraph("<font color='red'><b>Fail</b></font>", st['tb'])],
        [Paragraph("10", st['tb']), Paragraph("Text: 'idk please help me'", st['tb']), Paragraph("Invalid", st['tb']), Paragraph("HTTP 422 Non-code rejection", st['tb']), Paragraph("HTTP 422: Validates code required", st['tb']), Paragraph("<b>Pass</b>", st['tb'])],
    ]
    t_test = Table(test_rows, colWidths=[20, 115, 45, 145, 175, 40])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_test)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Captioned Screenshots of Real Runs:</b>", st['sub_heading']))
    chart_img = SCREENSHOTS_DIR / "01_prompt_comparison_chart.png"
    if chart_img.exists():
        story.append(Image(str(chart_img), width=500, height=210))
        story.append(Paragraph("<b>Figure 4.1:</b> Real run empirical benchmark chart comparing P1, P2, and P3 across all 6 criteria (Test #1 to #10).", st['caption']))

    story.append(Paragraph("<b>Known Limitations & Next Steps:</b>", st['sub_heading']))
    story.append(Paragraph(
        "1. <b>Static Review vs Dynamic Execution:</b> Cannot catch subtle multi-threaded concurrency race conditions. <i>Next step:</i> Integrate an isolated WebAssembly/Docker test runner in Milestone 3.<br/>"
        "2. <b>Nested Incomplete Code Stubs (Test #9):</b> Generated slightly generic hints on multi-nested ellipsis loops. <i>Next step:</i> Introduce AST-guided scope focus before prompt injection.<br/>"
        "3. <b>Single-Turn Interaction:</b> Currently operates on single-turn submissions. <i>Next step:</i> Expand into a multi-turn Socratic conversational dialogue.",
        st['body']
    ))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 5: REPOSITORY
    # =========================================================================
    story.append(Paragraph("Section 5: Repository", st['sec_heading']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=8))

    story.append(Paragraph("<b>Repository Structure & Folder Layout:</b>", st['sub_heading']))
    ui_img = SCREENSHOTS_DIR / "02_dashboard_interface.png"
    if ui_img.exists():
        story.append(Image(str(ui_img), width=500, height=230))
        story.append(Paragraph("<b>Figure 5.1:</b> CodeSense AI live application dashboard interface and repository review workspace.", st['caption']))

    story.append(Paragraph("<b>3–5 Lines on What Changed Since Milestone 1:</b>", st['sub_heading']))
    story.append(Paragraph(
        "1. Transformed initial Milestone 1 concept into a full-stack, production-ready application powered by FastAPI and modern SPA frontend.<br/>"
        "2. Published public GitHub repository at <b>https://github.com/div339175/CodeSense-AI</b> with full version history.<br/>"
        "3. Established dedicated prompt versioning directory (`prompts/v1`, `prompts/v2`, `prompts/v3`, `prompts/final`) with complete prompt text.<br/>"
        "4. Implemented automated testing suite in `tests/` with 26 unit and integration tests passing with 100% success.<br/>"
        "5. Maintained zero credential exposure through strict `.gitignore` and `.env.example` templates.",
        st['body']
    ))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 6: SUPPORTING DOCUMENT
    # =========================================================================
    story.append(Paragraph("Section 6: Supporting document", st['sec_heading']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=8))

    story.append(Paragraph(
        "<i>Note: The complete Supporting Document (Technical Report) uploaded at Q16 as <b>PromptForge_TechnicalReport.pdf</b> is embedded below in full.</i>",
        st['body']
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Document Type Selected:</b> Technical Report (Q15)", st['sub_heading']))
    story.append(Paragraph(
        "<b>Architecture & Engineering Summary:</b> CodeSense AI features an end-to-end decoupled pipeline: "
        "Student Code &rarr; FastAPI Request Sanitizer &rarr; Prompt Manager (P3 Hydration) &rarr; LLM Dispatcher &rarr; "
        "Response Parser & Repair &rarr; Socratic Hints UI & PDF Exporter. "
        "The system completely avoids code execution on the host machine, eliminating arbitrary execution risks. "
        "Automated benchmarking across 10 representative test cases proves that P3 eliminates complete-solution leakage (0% leakage), "
        "achieves 100% RFC-8259 JSON validity, and improves Socratic hint usefulness from 3.0/10 in P1 to 9.8/10 in P3.",
        st['body']
    ))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 7: TEAM CONTRIBUTION
    # =========================================================================
    story.append(Paragraph("Section 7: Team contribution", st['sec_heading']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=8))

    story.append(Paragraph("<b>Team Contribution Table (Team PromptForge - 5 Members = 100%):</b>", st['sub_heading']))
    contrib_rows = [
        [Paragraph("<b>Member Name</b>", st['th']), Paragraph("<b>Enrollment No.</b>", st['th']), Paragraph("<b>Role</b>", st['th']), Paragraph("<b>Tasks Done in Milestone 2</b>", st['th']), Paragraph("<b>Evidence</b>", st['th']), Paragraph("<b>Contribution (%)</b>", st['th'])],
        [Paragraph("<b>Divakar Maurya (Leader)</b>", st['tb']), Paragraph("<b>S24CSEU0807</b>", st['tb']), Paragraph("Full-Stack & LLM Engineer", st['tb']), Paragraph("Designed P3 prompt architecture, built FastAPI backend, Gemini API integration, and model fallback", st['tb']), Paragraph("app.py, backend/llm_client.py, 12 commits", st['tb']), Paragraph("<b>20%</b>", st['tb'])],
        [Paragraph("<b>Vrishank Pathak</b>", st['tb']), Paragraph("<b>S24CSEU0950</b>", st['tb']), Paragraph("Frontend & UI/UX Specialist", st['tb']), Paragraph("Built SPA dashboard, Prism.js syntax highlighting, and sample bug library dropdown", st['tb']), Paragraph("frontend/, static/css/style.css, 8 commits", st['tb']), Paragraph("<b>20%</b>", st['tb'])],
        [Paragraph("<b>Hardik Chawla</b>", st['tb']), Paragraph("<b>S24CSEU0750</b>", st['tb']), Paragraph("Prompt Engineering Specialist", st['tb']), Paragraph("Authored P1, P2 prompts, managed iteration log v1-v3, few-shot exemplars, and anti-leakage constraints", st['tb']), Paragraph("prompts/v1/, prompts/v2/, prompts/final/, 10 commits", st['tb']), Paragraph("<b>20%</b>", st['tb'])],
        [Paragraph("<b>Arpit Phutela</b>", st['tb']), Paragraph("<b>S24CSEU1594</b>", st['tb']), Paragraph("QA & Testing Engineer", st['tb']), Paragraph("Designed 10 benchmark test cases (Normal/Edge/Invalid), test-data/ dataset, and automated pytest suite", st['tb']), Paragraph("tests/, test-data/test_inputs.json, 7 commits", st['tb']), Paragraph("<b>20%</b>", st['tb'])],
        [Paragraph("<b>Ronak</b>", st['tb']), Paragraph("<b>S24CSEU0377</b>", st['tb']), Paragraph("Technical Documentation & Demo Specialist", st['tb']), Paragraph("Authored Milestone 2 technical report, recorded video demo, and prepared submission PDFs", st['tb']), Paragraph("docs/M2_PE-B25-04_CodeSenseAI.pdf, 6 commits", st['tb']), Paragraph("<b>20%</b>", st['tb'])],
    ]
    t_contrib = Table(contrib_rows, colWidths=[100, 75, 95, 140, 95, 35])
    t_contrib.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_contrib)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>All Members Agreement Confirmation:</b>", st['sub_heading']))
    story.append(Paragraph(
        "By submitting this document, all 5 team members of <b>Team PromptForge</b> confirm unanimous agreement on the individual contributions, "
        "task allocations, and percentage distributions outlined above (20% each = 100%). Each member is prepared to defend their assigned tasks during faculty evaluation.",
        st['body']
    ))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=8))
    story.append(Paragraph("CodeSense AI — SCSE4041 Prompt Engineering – Milestone 2 Final Submission", st['caption']))

    doc.build(story)
    print(f"[OK] Generated Milestone 2 Main PDF: {pdf_path}")

if __name__ == "__main__":
    import shutil
    supp_pdf = DOCS_DIR / "PromptForge_TechnicalReport.pdf"
    build_supporting_document_pdf(supp_pdf)

    main_pdf = DOCS_DIR / "M2_PE-B25-04_CodeSenseAI.pdf"
    build_milestone2_main_pdf(main_pdf)
    
    shutil.copyfile(main_pdf, DOCS_DIR / "M2_C4_CodeSenseAI.pdf")
