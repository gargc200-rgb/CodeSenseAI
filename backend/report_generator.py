"""
Report Generator Module for CodeSense AI
Generates downloadable Markdown and PDF analysis reports for students.
"""
from datetime import datetime
from io import BytesIO
from typing import Dict, Any

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

from backend.validator import CodeAnalysisResponse

class ReportGenerator:
    @staticmethod
    def generate_markdown(
        analysis: CodeAnalysisResponse,
        code: str,
        student_id: str = "Student",
        problem_description: str = ""
    ) -> str:
        """
        Creates a structured Markdown report.
        """
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            f"# CodeSense AI – Pedagogical Code Review Report",
            f"**Course:** Prompt Engineering (SCSE4041) | **Project ID:** C4",
            f"**Generated At:** {now_str}",
            f"**Student Reference:** {student_id}",
            f"**Programming Language:** {analysis.language}",
            f"**Prompt Version Used:** {analysis.prompt_version_used}",
            f"**Execution Provider:** {analysis.provider_used} ({analysis.execution_time_ms} ms)",
            "",
            "---",
            "",
            "## 1. Submitted Source Code",
            f"```{analysis.language.lower()}",
            code.strip(),
            "```",
            "",
        ]

        if problem_description:
            lines.extend([
                "**Student Problem Description:**",
                f"> {problem_description}",
                ""
            ])

        lines.extend([
            "## 2. Overall Assessment",
            f"{analysis.overall_assessment}",
            "",
            "## 3. Detected Issues & Learning Hints",
        ])

        if not analysis.issues:
            lines.append("🎉 **No issues detected!** The submitted code is syntactically sound and logically consistent.")
        else:
            for idx, issue in enumerate(analysis.issues, 1):
                lines.extend([
                    f"### Issue {idx}: {issue.issue}",
                    f"- **Severity:** `{issue.severity}`",
                    f"- **Concept to Revise:** `{issue.concept_to_revise}`",
                    f"- **Explanation:** {issue.explanation}",
                    f"- **Learning Hint (Socratic):** {issue.hint}",
                    ""
                ])

        lines.extend([
            "## 4. Positive Feedback",
            f"{analysis.positive_feedback}",
            "",
            "## 5. Recommended Next Step",
            f"{analysis.next_step}",
            "",
            "---",
            "*Report generated automatically by CodeSense AI – Fostering independent debugging without revealing solutions.*"
        ])

        return "\n".join(lines)

    @staticmethod
    def generate_pdf(
        analysis: CodeAnalysisResponse,
        code: str,
        student_id: str = "Student",
        problem_description: str = ""
    ) -> bytes:
        """
        Generates a professionally styled PDF report using ReportLab.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#1e293b"),
            spaceAfter=6
        )
        subtitle_style = ParagraphStyle(
            'DocSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#64748b"),
            spaceAfter=12
        )
        h2_style = ParagraphStyle(
            'Heading2',
            parent=styles['Heading2'],
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=12,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#334155")
        )
        code_style = ParagraphStyle(
            'CodeBlock',
            parent=styles['Code'],
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#0f172a"),
            backColor=colors.HexColor("#f8fafc"),
            borderColor=colors.HexColor("#e2e8f0"),
            borderWidth=1,
            borderPadding=6,
            spaceAfter=8
        )
        hint_style = ParagraphStyle(
            'HintBlock',
            parent=styles['Normal'],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#0369a1"),
            backColor=colors.HexColor("#f0f9ff"),
            borderColor=colors.HexColor("#bae6fd"),
            borderWidth=1,
            borderPadding=6,
            spaceAfter=6
        )

        elements = []

        # Header
        elements.append(Paragraph("CodeSense AI – Code Review Report", title_style))
        now_str = datetime.now().strftime("%B %d, %Y - %H:%M:%S")
        elements.append(Paragraph(f"Course: Prompt Engineering (SCSE4041) | Project ID: C4 | Date: {now_str}", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=10))

        # Metadata Table
        meta_data = [
            [Paragraph("<b>Target Language:</b>", body_style), Paragraph(analysis.language, body_style),
             Paragraph("<b>Prompt Version:</b>", body_style), Paragraph(f"{analysis.prompt_version_used}", body_style)],
            [Paragraph("<b>Student Ref:</b>", body_style), Paragraph(student_id, body_style),
             Paragraph("<b>Engine / Provider:</b>", body_style), Paragraph(f"{analysis.provider_used}", body_style)]
        ]
        meta_table = Table(meta_data, colWidths=[100, 160, 100, 160])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
            ('PADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 10))

        # Overall Assessment
        elements.append(Paragraph("1. Overall Assessment", h2_style))
        elements.append(Paragraph(analysis.overall_assessment, body_style))
        elements.append(Spacer(1, 8))

        # Submitted Code Snippet
        elements.append(Paragraph("2. Submitted Code Snippet", h2_style))
        clean_code = code.strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # Split lines if too long
        truncated_code = "\n".join(clean_code.splitlines()[:25])
        if len(clean_code.splitlines()) > 25:
            truncated_code += "\n... [snippet truncated for length]"
        elements.append(Paragraph(f"<pre>{truncated_code}</pre>", code_style))

        # Issues & Learning Hints
        elements.append(Paragraph("3. Detected Issues & Socratic Hints", h2_style))
        if not analysis.issues:
            elements.append(Paragraph("<b>No issues detected!</b> The code is clean and functioning.", body_style))
        else:
            for i, issue in enumerate(analysis.issues, 1):
                sev_color = "#dc2626" if issue.severity == "Critical" else ("#ea580c" if issue.severity == "High" else "#0284c7")
                issue_header = f"<b>Issue {i}: {issue.issue}</b> (<font color='{sev_color}'><b>{issue.severity}</b></font>)"
                elements.append(Paragraph(issue_header, body_style))
                elements.append(Paragraph(f"<b>Concept to Revise:</b> {issue.concept_to_revise}", body_style))
                elements.append(Paragraph(f"<b>Explanation:</b> {issue.explanation}", body_style))
                elements.append(Paragraph(f"<b>Learning Hint:</b> {issue.hint}", hint_style))
                elements.append(Spacer(1, 4))

        # Positive Feedback & Next Step
        elements.append(Paragraph("4. Positive Reinforcement", h2_style))
        elements.append(Paragraph(analysis.positive_feedback, body_style))
        elements.append(Spacer(1, 6))

        elements.append(Paragraph("5. Recommended Next Learning Step", h2_style))
        elements.append(Paragraph(analysis.next_step, body_style))
        elements.append(Spacer(1, 12))

        # Footer
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=6))
        elements.append(Paragraph("CodeSense AI – College Mini-Project (SCSE4041) – Educational Code Review Assistant", subtitle_style))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
