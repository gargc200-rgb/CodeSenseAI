"""
API Integration tests for CodeSense AI
"""
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Python" in data["supported_languages"]
    assert "P3" in data["available_prompts"]

def test_dashboard_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "CodeSense" in response.text

def test_prompts_list_endpoint():
    response = client.get("/api/prompts")
    assert response.status_code == 200
    data = response.json()
    assert "P1" in data["prompts"]
    assert "P2" in data["prompts"]
    assert "P3" in data["prompts"]

def test_prompt_detail_endpoint():
    response = client.get("/api/prompts/P3")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "P3"
    assert "SOCRATIC" in data["template"]

def test_analyze_endpoint_python():
    payload = {
        "code": "def add(a, b):\n    return a + b\nprint(add(2, 3))",
        "language": "Python",
        "prompt_version": "P3",
        "problem_description": "Add two numbers"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "Python"
    assert data["prompt_version_used"] == "P3"
    assert "overall_assessment" in data

def test_analyze_endpoint_empty_code_rejected():
    payload = {
        "code": "   ",
        "language": "Python"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 422 # FastAPI validation error

def test_analyze_endpoint_invalid_language():
    payload = {
        "code": "echo 'hello'",
        "language": "Bash"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 422

def test_compare_endpoint():
    payload = {
        "code": "total = 100\ncount = 0\navg = total / count",
        "language": "Python",
        "problem_description": "Calculate average"
    }
    response = client.post("/api/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "comparison" in data
    assert "P1" in data["comparison"]
    assert "P2" in data["comparison"]
    assert "P3" in data["comparison"]

def test_history_lifecycle():
    # Fetch history
    res = client.get("/api/history")
    assert res.status_code == 200
    assert "history" in res.json()

    # Clear history
    del_res = client.delete("/api/history")
    assert del_res.status_code == 200
    assert del_res.json()["message"] == "History cleared"

def test_export_report_markdown():
    payload = {
        "format": "markdown",
        "code": "x = 5",
        "student_id": "TestStudent",
        "analysis": {
            "overall_assessment": "Clean code",
            "language": "Python",
            "issues": [],
            "positive_feedback": "Great job",
            "next_step": "Try functions",
            "prompt_version_used": "P3",
            "execution_time_ms": 12.5,
            "provider_used": "mock"
        }
    }
    response = client.post("/api/export-report", json=payload)
    assert response.status_code == 200
    assert "CodeSense AI" in response.text
    assert "TestStudent" in response.text

def test_export_report_pdf():
    payload = {
        "format": "pdf",
        "code": "int a = 10;",
        "student_id": "TestStudent",
        "analysis": {
            "overall_assessment": "Valid C++ code",
            "language": "C++",
            "issues": [],
            "positive_feedback": "Correct syntax",
            "next_step": "Try pointers",
            "prompt_version_used": "P3",
            "execution_time_ms": 15.0,
            "provider_used": "mock"
        }
    }
    response = client.post("/api/export-report", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 1000 # Valid PDF bytes
