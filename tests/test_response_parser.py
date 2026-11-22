"""
Unit tests for CodeSense AI Response Parser
"""
from backend.response_parser import ResponseParser

def test_extract_json_from_markdown():
    raw_md = """Here is your review:
```json
{
  "overall_assessment": "Code has an error",
  "language": "Python",
  "issues": [],
  "positive_feedback": "Good job",
  "next_step": "Revise syntax"
}
```
Hope this helps!"""
    extracted = ResponseParser.extract_json_str(raw_md)
    assert extracted.startswith("{")
    assert extracted.endswith("}")

def test_repair_trailing_comma():
    malformed = '{"a": 1, "b": [1, 2, ], }'
    repaired = ResponseParser.repair_json_string(malformed)
    assert ", }" not in repaired
    assert ", ]" not in repaired

def test_parse_valid_json_response():
    valid_payload = """```json
{
  "overall_assessment": "Division by zero potential",
  "language": "Python",
  "issues": [
    {
      "issue": "ZeroDivisionError",
      "severity": "High",
      "explanation": "Cannot divide by 0",
      "hint": "Check with if statement",
      "concept_to_revise": "Conditionals"
    }
  ],
  "positive_feedback": "Proper variable naming",
  "next_step": "Practice if-else"
}
```"""
    resp, is_valid = ResponseParser.parse(valid_payload, "Python", "P3")
    assert is_valid is True
    assert resp.overall_assessment == "Division by zero potential"
    assert len(resp.issues) == 1
    assert resp.issues[0].severity == "High"

def test_parse_baseline_unstructured_text():
    unstructured = """Review:
- Bug in loop counter
- Code crashes on zero
Here is the corrected code:
```python
x = 10
```"""
    resp, is_valid = ResponseParser.parse(unstructured, "Python", "P1")
    assert is_valid is False
    assert len(resp.issues) >= 1
    assert resp.prompt_version_used == "P1"
