"""
PDF Generator for CodeSense AI Documentation
Builds docs/technical_report.pdf and docs/prompt_design_document.pdf
"""
import sys
import re
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"

def convert_md_to_pdf(md_path: Path, pdf_path: Path, title: str):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=14
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0284c7"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        leftIndent=15,
        spaceAfter=3
    )
    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Code'],
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=5,
        spaceBefore=4,
        spaceAfter=6
    )

    elements = []

    # Title & Header
    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph("Course: Prompt Engineering (SCSE4041) | Milestone 2 | Project ID: C4", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=12))

    lines = md_text.splitlines()
    in_code_block = False
    code_accumulator = []

    for line in lines:
        stripped = line.strip()

        # Handle Code Blocks
        if stripped.startswith("```"):
            if in_code_block:
                # End of code block
                full_code = "\n".join(code_accumulator)
                clean_code = full_code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                elements.append(Paragraph(f"<pre>{clean_code}</pre>", code_style))
                code_accumulator = []
                in_code_block = False
            else:
                in_code_block = True
                code_accumulator = []
            continue

        if in_code_block:
            code_accumulator.append(line)
            continue

        # Skip main title since we already added it
        if stripped.startswith("# ") and "CodeSense AI" in stripped:
            continue
        if stripped.startswith("## ") and ("Educational Code Review" in stripped or "Engineering Socratic" in stripped):
            continue

        # Headings
        if stripped.startswith("## "):
            h_text = stripped[3:].strip()
            elements.append(Paragraph(h_text, h1_style))
            elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=6))
        elif stripped.startswith("### "):
            h_text = stripped[4:].strip()
            elements.append(Paragraph(h_text, h2_style))
        elif stripped.startswith("- ") or stripped.startswith("* "):
            b_text = stripped[2:].strip()
            # Clean markdown bold
            b_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", b_text)
            b_text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", b_text)
            b_text = re.sub(r"`(.*?)`", r"<font name='Courier' color='#0369a1'>\1</font>", b_text)
            elements.append(Paragraph(f"• {b_text}", bullet_style))
        elif stripped.startswith("|") and stripped.endswith("|"):
            # Skip markdown table rows in body text rendering (already detailed in tables or text)
            continue
        elif stripped == "---":
            elements.append(Spacer(1, 4))
        elif stripped:
            p_text = stripped
            p_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", p_text)
            p_text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", p_text)
            p_text = re.sub(r"`(.*?)`", r"<font name='Courier' color='#0369a1'>\1</font>", p_text)
            elements.append(Paragraph(p_text, body_style))
        else:
            elements.append(Spacer(1, 3))

    doc.build(elements)
    print(f"[OK] Successfully built PDF: {pdf_path}")

if __name__ == "__main__":
    tech_md = DOCS_DIR / "technical_report.md"
    tech_pdf = DOCS_DIR / "technical_report.pdf"
    convert_md_to_pdf(tech_md, tech_pdf, "CodeSense AI – Technical Report")

    prompt_md = DOCS_DIR / "prompt_design_document.md"
    prompt_pdf = DOCS_DIR / "prompt_design_document.pdf"
    convert_md_to_pdf(prompt_md, prompt_pdf, "CodeSense AI – Prompt Design Document")
