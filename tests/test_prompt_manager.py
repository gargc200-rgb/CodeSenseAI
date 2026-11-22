"""
Unit tests for CodeSense AI Prompt Manager
"""
import pytest
from backend.prompt_manager import prompt_manager

def test_prompt_manager_loads_all_versions():
    versions = prompt_manager.list_versions()
    assert "P1" in versions
    assert "P2" in versions
    assert "P3" in versions

def test_get_prompt_text():
    p1 = prompt_manager.get_prompt_text("P1")
    p2 = prompt_manager.get_prompt_text("P2")
    p3 = prompt_manager.get_prompt_text("P3")

    assert "{language}" in p1
    assert "{code}" in p1
    assert "CRITICAL CONSTRAINT" in p2
    assert "SOCRATIC HINT GENERATION" in p3
    assert "ZERO SOLUTION LEAKAGE" in p3

def test_format_prompt_injection():
    formatted = prompt_manager.format_prompt(
        version_id="P3",
        language="Python",
        code="print('test')",
        problem_description="Test description"
    )
    assert "Python" in formatted
    assert "print('test')" in formatted
    assert "Test description" in formatted
    # Ensure template placeholders are replaced
    assert "{language}" not in formatted
    assert "{code}" not in formatted

def test_invalid_prompt_version():
    with pytest.raises(KeyError):
        prompt_manager.get_prompt_text("P99")
