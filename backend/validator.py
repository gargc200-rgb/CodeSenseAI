"""
Validation and data schema module for CodeSense AI
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator
from backend.config import SUPPORTED_LANGUAGES, MAX_CODE_LENGTH_CHARS, MAX_DESCRIPTION_LENGTH_CHARS

SeverityLevel = Literal["Critical", "High", "Medium", "Low", "No issue detected"]

class CodeIssue(BaseModel):
    issue: str = Field(..., description="Short title of the identified issue")
    severity: SeverityLevel = Field(..., description="Severity categorization of the issue")
    explanation: str = Field(..., description="Pedagogical explanation of why the issue occurs")
    hint: str = Field(..., description="Socratic guidance without revealing the complete solution")
    concept_to_revise: str = Field(..., description="Target programming concept for student revision")

class CodeAnalysisResponse(BaseModel):
    overall_assessment: str = Field(..., description="High-level assessment of code health and error presence")
    language: str = Field(..., description="Programming language analyzed")
    issues: List[CodeIssue] = Field(default_factory=list, description="List of detected code issues")
    positive_feedback: str = Field(..., description="Reinforcing feedback on what the student did right")
    next_step: str = Field(..., description="Suggested next learning step or practice topic")
    prompt_version_used: Optional[str] = Field("P3", description="Prompt version used (P1, P2, P3)")
    execution_time_ms: Optional[float] = Field(0.0, description="Processing duration in milliseconds")
    provider_used: Optional[str] = Field("auto", description="LLM provider that generated the response")

class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Source code submitted by the student")
    language: str = Field(..., description="Programming language (Python, C++, Java)")
    problem_description: Optional[str] = Field(None, description="Optional description of the assigned problem or intended task")
    prompt_version: Optional[str] = Field("P3", description="Prompt version to execute (P1, P2, P3)")
    provider: Optional[str] = Field(None, description="Optional override for LLM provider")

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Submitted code cannot be empty.")
        if len(trimmed) > MAX_CODE_LENGTH_CHARS:
            raise ValueError(f"Submitted code exceeds maximum limit of {MAX_CODE_LENGTH_CHARS} characters.")
        return trimmed

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        standardized = v.strip().title()
        # Handle C++ variants
        if standardized.lower() in ["c++", "cpp"]:
            return "C++"
        if standardized.lower() in ["python", "py"]:
            return "Python"
        if standardized.lower() in ["java"]:
            return "Java"
        
        valid_langs = ", ".join(SUPPORTED_LANGUAGES)
        raise ValueError(f"Unsupported programming language '{v}'. Supported languages are: {valid_langs}")

    @field_validator("problem_description")
    @classmethod
    def validate_problem_description(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) > MAX_DESCRIPTION_LENGTH_CHARS:
            raise ValueError(f"Problem description exceeds maximum limit of {MAX_DESCRIPTION_LENGTH_CHARS} characters.")
        return v

    @field_validator("prompt_version")
    @classmethod
    def validate_prompt_version(cls, v: Optional[str]) -> str:
        version = (v or "P3").upper().strip()
        if version not in ["P1", "P2", "P3"]:
            raise ValueError("Prompt version must be one of: P1, P2, P3")
        return version

class PromptCompareRequest(BaseModel):
    code: str = Field(..., description="Source code to compare across P1, P2, and P3")
    language: str = Field(..., description="Programming language (Python, C++, Java)")
    problem_description: Optional[str] = Field(None, description="Optional problem context")
