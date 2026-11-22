"""
Generates visual UI screenshots and layout overviews for documentation and README.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

def create_dashboard_screenshot():
    width, height = 1200, 750
    img = Image.new("RGB", (width, height), color="#0f172a")
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (width, 60)], fill="#0284c7")
    draw.text((30, 18), "CodeSense AI – Educational Code Review Assistant (SCSE4041 - Milestone 2)", fill="#ffffff")
    draw.text((950, 20), "Project ID: C4 | Anti-Leakage Active", fill="#e0f2fe")

    # Left Panel - Editor
    draw.rounded_rectangle([(40, 90), (620, 680)], radius=10, fill="#1e293b", outline="#334155", width=2)
    draw.rectangle([(40, 90), (620, 135)], fill="#0f172a")
    draw.text((60, 105), "Language: Python  |  Prompt: P3 (Final Optimized)  |  student_code.py", fill="#38bdf8")
    
    code_sample = [
        "total_marks = 450",
        "student_count = int(input('Enter number of students: '))",
        "",
        "# Potential ZeroDivisionError if user inputs 0:",
        "class_average = total_marks / student_count",
        "print('Class average is:', class_average)"
    ]
    y = 155
    for line in code_sample:
        draw.text((60, y), line, fill="#f8fafc")
        y += 24

    # Analyze Button
    draw.rounded_rectangle([(60, 610), (600, 655)], radius=8, fill="#0284c7")
    draw.text((260, 625), "⚡ ANALYZE CODE (P3 SOCRATIC)", fill="#ffffff")

    # Right Panel - Results Dashboard
    draw.rounded_rectangle([(650, 90), (1160, 680)], radius=10, fill="#ffffff", outline="#e2e8f0", width=2)
    draw.text((670, 110), "REVIEW RESULTS: 0% SOLUTION LEAKAGE GUARANTEED", fill="#0369a1")

    # Overall Assessment Card
    draw.rounded_rectangle([(670, 140), (1140, 210)], radius=6, fill="#f8fafc", outline="#e2e8f0")
    draw.text((680, 150), "1. Overall Assessment", fill="#64748b")
    draw.text((680, 170), "Code calculates an average, but crashes when input is 0.", fill="#0f172a")

    # Detected Issue Card
    draw.rounded_rectangle([(670, 225), (1140, 395)], radius=6, fill="#fff7ed", outline="#fdba74")
    draw.text((680, 235), "2. Issue: ZeroDivisionError [SEVERITY: HIGH]", fill="#c2410c")
    draw.text((680, 260), "Explanation: Division by zero terminates runtime immediately.", fill="#7c2d12")
    draw.rounded_rectangle([(680, 290), (1130, 380)], radius=6, fill="#f0f9ff", outline="#7dd3fc")
    draw.text((690, 305), "💡 SOCRATIC LEARNING HINT (Zero-Leakage):", fill="#0369a1")
    draw.text((690, 330), "What conditional check ('if') could you place before division", fill="#0c4a6e")
    draw.text((690, 350), "to ensure student_count is not zero?", fill="#0c4a6e")

    # Positive Feedback Card
    draw.rounded_rectangle([(670, 410), (1140, 485)], radius=6, fill="#f0fdf4", outline="#86efac")
    draw.text((680, 420), "3. Positive Feedback", fill="#15803d")
    draw.text((680, 445), "Great variable naming and accurate arithmetic division syntax.", fill="#166534")

    # Next Step Card
    draw.rounded_rectangle([(670, 500), (1140, 575)], radius=6, fill="#eef2ff", outline="#a5b4fc")
    draw.text((680, 510), "4. Recommended Next Step", fill="#4338ca")
    draw.text((680, 535), "Practice writing defensive guard conditions before computations.", fill="#3730a3")

    # Action Buttons
    draw.rounded_rectangle([(670, 610), (890, 655)], radius=8, fill="#f1f5f9", outline="#cbd5e1")
    draw.text((710, 625), "📄 Export Markdown", fill="#334155")
    draw.rounded_rectangle([(910, 610), (1140, 655)], radius=8, fill="#0284c7")
    draw.text((950, 625), "📥 Export PDF Report", fill="#ffffff")

    out_path = SCREENSHOTS_DIR / "02_dashboard_interface.png"
    img.save(out_path)
    print(f"[OK] Generated UI overview screenshot: {out_path}")

if __name__ == "__main__":
    create_dashboard_screenshot()
