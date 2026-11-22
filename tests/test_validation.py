"""
Unit tests for CodeSense AI Input Validation and Data Schemas
"""
import pytest
from pydantic import ValidationError
from backend.validator import CodeAnalysisRequest, CodeIssue, CodeAnalysisResponse

def test_valid_request():
    req = CodeAnalysisRequest(
        code="print('Hello World')",
        language="Python",
        prompt_version="P3"
    )
    assert req.code == "print('Hello World')"
    assert req.language == "Python"
    assert req.prompt_version == "P3"

def test_language_normalization():
    req_cpp = CodeAnalysisRequest(code="int x = 5;", language="cpp")
    assert req_cpp.language == "C++"

    req_java = CodeAnalysisRequest(code="System.out.println();", language="JAVA")
    assert req_java.language == "Java"

def test_unsupported_language_rejection():
    with pytest.raises(ValidationError):
        CodeAnalysisRequest(code="fn main() {}", language="Rust")

def test_empty_code_rejection():
    with pytest.raises(ValidationError):
        CodeAnalysisRequest(code="   ", language="Python")

def test_invalid_prompt_version_rejection():
    with pytest.raises(ValidationError):
        CodeAnalysisRequest(code="x = 1", language="Python", prompt_version="P99")

def test_code_issue_model():
    issue = CodeIssue(
        issue="Division by Zero",
        severity="High",
        explanation="Denominator is zero",
        hint="Check if denominator is 0",
        concept_to_revise="Conditionals"
    )
    assert issue.severity == "High"
    assert issue.issue == "Division by Zero"

def test_code_analysis_response_model():
    resp = CodeAnalysisResponse(
        overall_assessment="Good code with minor bug",
        language="Python",
        issues=[],
        positive_feedback="Great syntax",
        next_step="Keep practicing",
        prompt_version_used="P3"
    )
    assert resp.language == "Python"
    assert len(resp.issues) == 0
