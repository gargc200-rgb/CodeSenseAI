"""
Response Parser Module for CodeSense AI
Extracts, repairs, validates, and normalizes LLM outputs into structured schemas.
"""
import json
import re
from typing import Dict, Any, Tuple
from backend.validator import CodeAnalysisResponse, CodeIssue

class ResponseParser:
    @staticmethod
    def extract_json_str(raw_text: str) -> str:
        """
        Extract the JSON substring from raw model output, stripping markdown code blocks.
        """
        text = raw_text.strip()
        
        # Match ```json ... ``` or ``` ... ```
        json_block_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if json_block_match:
            return json_block_match.group(1).strip()
        
        # Match outermost curly braces
        curly_match = re.search(r"(\{.*\})", text, re.DOTALL)
        if curly_match:
            return curly_match.group(1).strip()
            
        return text

    @staticmethod
    def repair_json_string(json_str: str) -> str:
        """
        Basic heuristic repair for common LLM JSON defects:
        - Trailing commas before } or ]
        - Python None/True/False to null/true/false
        """
        s = json_str
        s = re.sub(r",\s*([\]}])", r"\1", s)
        s = re.sub(r"\bNone\b", "null", s)
        s = re.sub(r"\bTrue\b", "true", s)
        s = re.sub(r"\bFalse\b", "false", s)
        return s

    @classmethod
    def parse_baseline_unstructured(
        cls,
        raw_text: str,
        language: str
    ) -> CodeAnalysisResponse:
        """
        Normalize unstructured text output from P1 (Baseline prompt)
        into the CodeSense AI schema so it can be compared.
        """
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        
        # Detect any explicit code blocks that leaked
        leaked_code_blocks = re.findall(r"```(?:\w+)?\n?(.*?)```", raw_text, re.DOTALL)
        has_code_leakage = len(leaked_code_blocks) > 0
        
        overall = "Baseline review provided free-form feedback."
        if lines:
            overall = lines[0]
            if len(overall) > 200:
                overall = overall[:197] + "..."

        issues = []
        # Attempt to split bullet points
        bullet_points = [l for l in lines if l.startswith(("-", "*", "1.", "2.", "3.", "•"))]
        
        if bullet_points:
            for bp in bullet_points[:4]:
                clean_bp = re.sub(r"^[-*•\d.]+\s*", "", bp)
                issues.append(
                    CodeIssue(
                        issue=clean_bp[:60] if len(clean_bp) > 60 else clean_bp,
                        severity="High" if any(w in clean_bp.lower() for w in ["error", "crash", "invalid", "fail"]) else "Medium",
                        explanation=clean_bp,
                        hint="Review the error description above and check related syntax rules." + (" [Note: Baseline prompt revealed direct code]" if has_code_leakage else ""),
                        concept_to_revise="General Syntax & Debugging"
                    )
                )
        else:
            # Fallback single issue
            issues.append(
                CodeIssue(
                    issue="Unstructured Issue Identified",
                    severity="Medium",
                    explanation=raw_text[:300] if len(raw_text) > 300 else raw_text,
                    hint="Consider breaking down the logic step-by-step.",
                    concept_to_revise="Code Review & Debugging"
                )
            )

        return CodeAnalysisResponse(
            overall_assessment=overall,
            language=language,
            issues=issues,
            positive_feedback="Submitted code was reviewed. Baseline prompt provides minimal positive encouragement.",
            next_step="Try using Prompt P3 (Final Optimized) for pedagogical Socratic hints and zero code leakage.",
            prompt_version_used="P1"
        )

    @classmethod
    def parse(
        cls,
        raw_output: str,
        language: str,
        prompt_version: str = "P3"
    ) -> Tuple[CodeAnalysisResponse, bool]:
        """
        Parses raw model output.
        Returns: (parsed_response, is_valid_json)
        """
        clean_json_str = cls.extract_json_str(raw_output)
        clean_json_str = cls.repair_json_string(clean_json_str)

        try:
            data = json.loads(clean_json_str)
            # Ensure required fields have sensible defaults if missing
            if not isinstance(data, dict):
                raise ValueError("Parsed JSON root is not an object.")

            data.setdefault("language", language)
            data.setdefault("overall_assessment", "Code review completed.")
            data.setdefault("positive_feedback", "Good effort attempting the problem.")
            data.setdefault("next_step", "Continue practicing programming exercises.")
            data.setdefault("prompt_version_used", prompt_version)

            # Normalize issues list
            raw_issues = data.get("issues", [])
            valid_issues = []
            valid_severities = {"Critical", "High", "Medium", "Low", "No issue detected"}

            for item in raw_issues:
                if isinstance(item, dict):
                    sev = item.get("severity", "Medium")
                    if sev not in valid_severities:
                        # Attempt capitalization match
                        sev_match = next((v for v in valid_severities if v.lower() == str(sev).lower()), "Medium")
                        sev = sev_match

                    valid_issues.append(
                        CodeIssue(
                            issue=str(item.get("issue", "Issue identified")),
                            severity=sev, # type: ignore
                            explanation=str(item.get("explanation", "Potential problem detected.")),
                            hint=str(item.get("hint", "Examine this section carefully.")),
                            concept_to_revise=str(item.get("concept_to_revise", "Programming fundamentals"))
                        )
                    )

            data["issues"] = [i.model_dump() for i in valid_issues]
            parsed = CodeAnalysisResponse(**data)
            return parsed, True

        except (json.JSONDecodeError, ValueError):
            # If prompt was P1 or model returned conversational text
            if prompt_version == "P1":
                return cls.parse_baseline_unstructured(raw_output, language), False
            
            # For P2 or P3 fallback if model fails JSON formatting
            fallback = cls.parse_baseline_unstructured(raw_output, language)
            fallback.prompt_version_used = prompt_version
            return fallback, False
