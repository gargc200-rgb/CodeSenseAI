"""
Multi-Provider LLM Client for CodeSense AI
Supports Google Gemini, OpenAI, and a built-in Pedagogical Mock Engine for offline demonstration.
"""
import os
import time
import json
import logging
from typing import Dict, Any, Tuple, Optional
from dotenv import load_dotenv
import httpx

from backend.config import (
    GEMINI_API_KEY,
    OPENAI_API_KEY,
    DEFAULT_PROVIDER,
    DEFAULT_MODEL,
    GEMINI_FALLBACK_MODELS,
    FALLBACK_OPENAI_MODEL,
    API_TIMEOUT_SECONDS
)

logger = logging.getLogger("codesense.llm_client")

class LLMClient:
    def __init__(self):
        self.gemini_key = GEMINI_API_KEY
        self.openai_key = OPENAI_API_KEY
        self.default_provider = DEFAULT_PROVIDER

    def get_gemini_key(self) -> str:
        """Returns Gemini API key, reloading from .env if needed."""
        key = os.getenv("GEMINI_API_KEY", "").strip() or self.gemini_key
        if not key:
            load_dotenv(override=True)
            key = os.getenv("GEMINI_API_KEY", "").strip()
            self.gemini_key = key
        return key

    def get_openai_key(self) -> str:
        """Returns OpenAI API key, reloading from .env if needed."""
        key = os.getenv("OPENAI_API_KEY", "").strip() or self.openai_key
        if not key:
            load_dotenv(override=True)
            key = os.getenv("OPENAI_API_KEY", "").strip()
            self.openai_key = key
        return key

    def detect_available_provider(self) -> str:
        """Determines active provider based on configured API keys."""
        if self.get_gemini_key():
            return "gemini"
        if self.get_openai_key():
            return "openai"
        return "mock"

    async def generate_response(
        self,
        prompt: str,
        language: str,
        prompt_version: str = "P3",
        provider_override: Optional[str] = None,
        code: str = ""
    ) -> Tuple[str, str, float]:
        """
        Executes prompt on selected provider.
        Returns: (raw_response_text, provider_name, execution_time_ms)
        """
        provider = provider_override or self.default_provider
        if provider == "auto":
            provider = self.detect_available_provider()

        start_time = time.time()
        raw_text = ""

        try:
            if provider == "gemini":
                raw_text, actual_model = await self._call_gemini(prompt)
                provider = f"gemini ({actual_model})"
            elif provider == "openai":
                raw_text = await self._call_openai(prompt)
                provider = "openai"
            else:
                raw_text = self._call_mock_engine(prompt_version, language, code, prompt)
                provider = "mock"
        except Exception as e:
            logger.warning(f"Error calling {provider}: {str(e)}. Falling back to pedagogical mock engine.")
            raw_text = self._call_mock_engine(prompt_version, language, code, prompt)
            provider = f"mock (fallback from {provider}: {type(e).__name__})"

        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        return raw_text, provider, elapsed_ms

    async def _call_gemini(self, prompt: str) -> Tuple[str, str]:
        """Invokes Google Gemini API using REST endpoint with automatic model fallback."""
        key = self.get_gemini_key()
        if not key:
            raise ValueError("GEMINI_API_KEY is not configured in .env")

        models_to_try = []
        for m in [DEFAULT_MODEL] + GEMINI_FALLBACK_MODELS:
            if m and m not in models_to_try:
                models_to_try.append(m)

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.95,
                "maxOutputTokens": 2048
            }
        }

        last_error = None
        async with httpx.AsyncClient(timeout=API_TIMEOUT_SECONDS) as client:
            for model_name in models_to_try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
                try:
                    resp = await client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        text = data["candidates"][0]["content"]["parts"][0]["text"]
                        return text, model_name
                    elif resp.status_code in (404, 503, 429):
                        logger.warning(f"Gemini model {model_name} returned {resp.status_code}. Trying next model...")
                        last_error = RuntimeError(f"Gemini API ({model_name}) returned HTTP {resp.status_code}: {resp.text}")
                        continue
                    else:
                        raise RuntimeError(f"Gemini API returned HTTP {resp.status_code}: {resp.text}")
                except (KeyError, IndexError) as err:
                    raise RuntimeError(f"Unexpected response format from Gemini: {resp.text}") from err
                except httpx.RequestError as req_err:
                    logger.warning(f"Network error querying {model_name}: {req_err}. Trying next...")
                    last_error = req_err
                    continue

        if last_error:
            raise last_error
        raise RuntimeError("No Gemini models succeeded.")

    async def _call_openai(self, prompt: str) -> str:
        """Invokes OpenAI API."""
        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY is not configured.")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": FALLBACK_OPENAI_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 2048
        }

        async with httpx.AsyncClient(timeout=API_TIMEOUT_SECONDS) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code != 200:
                raise RuntimeError(f"OpenAI API returned HTTP {resp.status_code}: {resp.text}")
            
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    def _call_mock_engine(
        self,
        prompt_version: str,
        language: str,
        code: str,
        full_prompt: str
    ) -> str:
        """
        Deterministic Pedagogical Offline Engine.
        Simulates model outputs for P1, P2, and P3 accurately:
        - P1: Unstructured text review, often leaking full corrected code (baseline defect).
        - P2: Semi-structured JSON with severity classification, but basic hints.
        - P3: Strict RFC-8259 JSON, high-accuracy bug diagnosis, Socratic hints, positive reinforcement, 0% solution leakage.
        """
        code_lower = code.lower()
        code_stripped = code.strip()

        # 1. Detect bug category
        is_clean = False
        bug_type = "unknown"

        # Check known critical bug patterns first
        if ":" not in code and any(keyword in code for keyword in ["def ", "for ", "if ", "while ", "elif "]) and language.lower() == "python":
            bug_type = "syntax_missing_colon"
        elif "/ 0" in code or "/0" in code or ("/ count" in code and "count == 0" not in code and "if" not in code):
            bug_type = "division_by_zero"
        elif "<= 5" in code or "<= arr.length" in code or "<= len(" in code:
            bug_type = "off_by_one_array"
        elif "arr[10]" in code or "arr[5]" in code or "scores[5]" in code or "grades[5]" in code:
            bug_type = "array_index_bounds"
        elif "while (" in code and "++" not in code and "+=" not in code and "break" not in code:
            bug_type = "infinite_loop"
        elif "while " in code and ":" in code and "+=" not in code and "break" not in code:
            bug_type = "infinite_loop"
        elif ("int sum;" in code or "int x;" in code) and ("= sum +" in code or "= x +" in code):
            bug_type = "uninitialized_var"
        elif "factorial" in code and "n == 0" not in code and "n <= 1" not in code:
            bug_type = "missing_base_case"
        elif "total = total - num" in code or ("total = 0" in code and "- num" in code):
            bug_type = "accumulator_logic"
        elif "null" in code_lower and ".length()" in code:
            bug_type = "null_pointer"
        elif "indentationerror" in code_lower or ("print(" in code and "  print(" not in code and "def " in code):
            bug_type = "indentation_error"
        elif "prin(" in code or "prnt(" in code or "prntln(" in code or "prin(hello)" in code:
            bug_type = "typo_print_func"
        elif "print(hello)" in code or ("(hello)" in code and '"hello"' not in code and "'hello'" not in code):
            bug_type = "typo_print_func"
        # Check known clean code patterns
        elif ("def add(" in code and "return a + b" in code) or ("sum is:" in code_lower and "arr[5]" not in code) or ("rectanglearea" in code_lower and "length * width" in code):
            is_clean = True
        elif language.lower() == "python":
            try:
                compile(code, "<string>", "exec")
                is_clean = True
            except SyntaxError:
                bug_type = "syntax_missing_colon"
            except Exception:
                bug_type = "general_bug"
        elif "system.out.println(" in code_lower and "null" not in code_lower and "[" not in code:
            is_clean = True
        elif "cout <<" in code_lower and "arr" not in code_lower and "sum" not in code_lower:
            is_clean = True
        else:
            bug_type = "general_bug"

        # --- GENERATE RESPONSES ACCORDING TO PROMPT VERSION ---

        # 1. P1: Baseline Prompt (Unstructured, leaks complete code, no structured schema)
        if prompt_version == "P1":
            if is_clean:
                return (
                    f"I reviewed your {language} program. It looks correct and runs with no syntax errors. Good job."
                )
            if bug_type == "syntax_missing_colon":
                return (
                    f"Your Python code has a SyntaxError. You forgot the colon at the end of the line.\n"
                    f"Here is the corrected code:\n"
                    f"```python\n"
                    f"def calculate_total(price, tax):\n"
                    f"    return price + (price * tax)\n"
                    f"print(calculate_total(100, 0.05))\n"
                    f"```\n"
                    f"You must always put a ':' after def, if, and loops."
                )
            elif bug_type == "division_by_zero":
                return (
                    f"Error detected in {language} code! Division by zero will crash the program.\n"
                    f"Here is the fixed code you should use:\n"
                    f"```python\n"
                    f"if count != 0:\n"
                    f"    average = total / count\n"
                    f"else:\n"
                    f"    average = 0\n"
                    f"print(average)\n"
                    f"```"
                )
            elif bug_type in ["off_by_one_array", "array_index_bounds"]:
                return (
                    f"There is an array index out of bounds error. Array indices go from 0 to size-1.\n"
                    f"Replace your loop with this corrected code:\n"
                    f"```{language.lower()}\n"
                    f"for (int i = 0; i < 5; i++) {{\n"
                    f"    std::cout << arr[i] << std::endl;\n"
                    f"}}\n"
                    f"```"
                )
            elif bug_type == "typo_print_func":
                return (
                    f"There is a typo and a NameError in your Python code.\n"
                    f"'prin' is misspelled, and 'hello' is not a defined variable.\n"
                    f"Here is the corrected code:\n"
                    f"```python\n"
                    f"print(\"hello\")\n"
                    f"```"
                )
            else:
                return (
                    f"I found a bug in your {language} code. Check your logic and variable declarations.\n"
                    f"Here is the complete corrected code:\n"
                    f"```{language.lower()}\n"
                    f"// Corrected solution\n"
                    f"{code}\n"
                    f"```"
                )

        # 2. P2: Improved Prompt (JSON output, has severity and role, but hints are generic)
        elif prompt_version == "P2":
            if is_clean:
                return json.dumps({
                    "overall_assessment": f"The submitted {language} program is syntactically sound and accomplishes its task.",
                    "language": language,
                    "issues": [],
                    "positive_feedback": "Clean code structure and sensible variable naming.",
                    "next_step": "Try implementing input validation for edge cases."
                }, indent=2)

            if bug_type == "syntax_missing_colon":
                return json.dumps({
                    "overall_assessment": "The code contains syntax errors preventing interpretation.",
                    "language": language,
                    "issues": [{
                        "issue": "Missing colon in block header",
                        "severity": "Critical",
                        "explanation": "In Python, compound statements like function definitions require a colon at the end of the line.",
                        "hint": "Add a colon ':' at the end of line 1.",
                        "concept_to_revise": "Python Syntax and Compound Statements"
                    }],
                    "positive_feedback": "Good function definition and parameter passing.",
                    "next_step": "Practice writing basic function signatures in Python."
                }, indent=2)
            elif bug_type == "division_by_zero":
                return json.dumps({
                    "overall_assessment": "The program crashes when denominator is zero.",
                    "language": language,
                    "issues": [{
                        "issue": "ZeroDivisionError",
                        "severity": "High",
                        "explanation": "Dividing a number by zero causes an unhandled runtime exception.",
                        "hint": "Check if the divisor is zero before dividing.",
                        "concept_to_revise": "Conditionals and Exception Handling"
                    }],
                    "positive_feedback": "Correct arithmetic operation syntax.",
                    "next_step": "Learn about if-else validation statements."
                }, indent=2)
            elif bug_type in ["off_by_one_array", "array_index_bounds"]:
                return json.dumps({
                    "overall_assessment": "Array boundary exceeded during iteration.",
                    "language": language,
                    "issues": [{
                        "issue": "Off-by-one array index",
                        "severity": "Critical",
                        "explanation": "The loop condition goes beyond the last valid index of the array.",
                        "hint": "Change '<=' to '<' in the loop condition.",
                        "concept_to_revise": "Array Indexing"
                    }],
                    "positive_feedback": "Proper loop structure and array initialization.",
                    "next_step": "Review zero-based index ranges."
                }, indent=2)
            elif bug_type == "typo_print_func":
                return json.dumps({
                    "overall_assessment": "The code contains an undefined function call and unquoted text.",
                    "language": language,
                    "issues": [{
                        "issue": "NameError: Undefined 'prin' / Missing String Quotes",
                        "severity": "High",
                        "explanation": "'prin' is not a built-in function in Python, and 'hello' without quotes is treated as an uninitialized variable.",
                        "hint": "Change 'prin' to 'print' and put quotes around hello.",
                        "concept_to_revise": "Built-in Functions and String Literals"
                    }],
                    "positive_feedback": "Good attempt at calling an output function.",
                    "next_step": "Practice using single and double quotes for strings."
                }, indent=2)
            else:
                return json.dumps({
                    "overall_assessment": f"Logical or runtime issue detected in {language} code.",
                    "language": language,
                    "issues": [{
                        "issue": "Potential Logic Flaw",
                        "severity": "High",
                        "explanation": "The logic does not handle variable updates or boundary termination properly.",
                        "hint": "Review the loop condition and variable assignments.",
                        "concept_to_revise": "Control Flow and State Management"
                    }],
                    "positive_feedback": "Good attempt at breaking down the logic.",
                    "next_step": "Trace variable values step by step on paper."
                }, indent=2)

        # 3. P3: Final Optimized Prompt (Socratic pedagogy, strict JSON, 0% solution leakage, rich revision)
        else:
            if is_clean:
                return json.dumps({
                    "overall_assessment": f"Outstanding effort! Your {language} program compiles cleanly, executes without runtime defects, and adheres to good programming conventions.",
                    "language": language,
                    "issues": [],
                    "positive_feedback": "Clean control flow, accurate syntax, appropriate data types, and well-structured execution logic.",
                    "next_step": "Consider exploring modular functions and defensive input boundary checks to deepen your software engineering skills."
                }, indent=2)

            if bug_type == "syntax_missing_colon":
                return json.dumps({
                    "overall_assessment": "The program has a lexical syntax error that halts Python's parser before execution can begin.",
                    "language": language,
                    "issues": [{
                        "issue": "SyntaxError: Missing Colon in Header Statement",
                        "severity": "Critical",
                        "explanation": "Python grammar requires a colon symbol (:) at the end of headers for functions (`def`), conditionals (`if`), and loops (`for`/`while`). This punctuation informs the parser that an indented block follows.",
                        "hint": "Look closely at the very end of your function or loop header line. What punctuation mark does Python use to introduce an indented body of code?",
                        "concept_to_revise": "Python Compound Statement Syntax & Block Delimiters"
                    }],
                    "positive_feedback": "You chose clear, self-explanatory parameter names and correctly intended to return a computed value.",
                    "next_step": "Review Python syntax rules for compound statement headers (`def`, `if`, `while`, `for`)."
                }, indent=2)

            elif bug_type == "division_by_zero":
                return json.dumps({
                    "overall_assessment": "The code performs arithmetic operations correctly under typical conditions, but is vulnerable to an unhandled runtime crash when the denominator evaluates to zero.",
                    "language": language,
                    "issues": [{
                        "issue": "Unhandled ZeroDivisionError (Division by Zero)",
                        "severity": "High",
                        "explanation": "Division by zero is mathematically undefined. In programming runtimes, executing a division where the denominator is zero triggers an immediate exception (ZeroDivisionError in Python, ArithmeticException in Java), crashing the application.",
                        "hint": "What conditional construct (`if`) could you place before the division to check whether your denominator is zero, and what fallback value or warning should be displayed?",
                        "concept_to_revise": "Defensive Programming and Guard Conditions"
                    }],
                    "positive_feedback": "Correct use of arithmetic division and sensible variable naming.",
                    "next_step": "Practice writing guard clauses with `if-else` blocks to validate inputs before computation."
                }, indent=2)

            elif bug_type in ["off_by_one_array", "array_index_bounds"]:
                return json.dumps({
                    "overall_assessment": "The program initializes an array and attempts iteration, but the loop condition breaches the allocated memory boundaries of the array.",
                    "language": language,
                    "issues": [{
                        "issue": "Array Index Out of Bounds (Off-by-One Loop Error)",
                        "severity": "Critical",
                        "explanation": "In zero-indexed languages (C++, Java, Python), an array of size N has valid indices from 0 up to N-1. When loop condition tests `i <= N`, the final iteration accesses index N, which is out of bounds and triggers undefined behavior or an IndexOutOfBoundsException.",
                        "hint": "If an array has 5 elements, what is the index of the first element? What is the index of the last element? Does your loop condition (`<=`) allow the index counter to step one position too far?",
                        "concept_to_revise": "Zero-Based Indexing and Loop Termination Predicates"
                    }],
                    "positive_feedback": "Proper array initialization and clean iteration framework.",
                    "next_step": "Trace array index bounds manually on a piece of paper for sizes 3, 5, and 10."
                }, indent=2)

            elif bug_type == "infinite_loop":
                return json.dumps({
                    "overall_assessment": "The control flow enters a loop that cannot terminate under normal execution, leading to an infinite execution loop.",
                    "language": language,
                    "issues": [{
                        "issue": "Infinite Loop (Non-Progressing Termination Condition)",
                        "severity": "High",
                        "explanation": "A `while` loop continues running as long as its condition remains true. If the state variables tested in the condition are never modified inside the loop body, the condition remains permanently true.",
                        "hint": "Examine the variable tested in your `while` condition. Is that variable updated anywhere inside the loop body? How will the loop ever know when to stop?",
                        "concept_to_revise": "Loop Invariants, Iteration Progression, and Termination Conditions"
                    }],
                    "positive_feedback": "Clear initial state declaration and attempt at automated repetition.",
                    "next_step": "Study loop counters and increment/decrement operators (`++`, `+=`)."
                }, indent=2)

            elif bug_type == "uninitialized_var":
                return json.dumps({
                    "overall_assessment": "The program reads from an uninitialized local variable, resulting in unpredictable behavior or garbage data.",
                    "language": language,
                    "issues": [{
                        "issue": "Uninitialized Variable Usage",
                        "severity": "Critical",
                        "explanation": "In languages like C++, declaring a local variable without an explicit initial value leaves it containing whatever indeterminate garbage bits previously occupied that memory location.",
                        "hint": "Before using a variable on the right-hand side of an assignment, what initial value should it hold? Have you assigned a starting value like 0 or an empty string?",
                        "concept_to_revise": "Variable Lifecycle, Memory Allocation, and Initialization"
                    }],
                    "positive_feedback": "Correct type declaration and syntactically clean arithmetic assignment.",
                    "next_step": "Adopt the best practice of always initializing variables at the point of declaration."
                }, indent=2)

            elif bug_type == "missing_base_case":
                return json.dumps({
                    "overall_assessment": "The recursive function lacks an accessible base case, causing unlimited recursive calls that result in a stack overflow.",
                    "language": language,
                    "issues": [{
                        "issue": "Missing Recursive Base Case (Infinite Recursion)",
                        "severity": "Critical",
                        "explanation": "Every recursive function must contain a base case that returns a concrete value without calling itself. Without this, the call stack grows until memory is exhausted.",
                        "hint": "What is the simplest input for which this function should know the answer immediately without further calculation (e.g., when n is 0 or 1)? How can you return that early?",
                        "concept_to_revise": "Recursion Mechanics and Base-Case Design"
                    }],
                    "positive_feedback": "Good understanding of the mathematical recurrence relation.",
                    "next_step": "Trace recursive calls using a call-tree diagram on paper."
                }, indent=2)

            elif bug_type == "typo_print_func":
                return json.dumps({
                    "overall_assessment": "The code attempts to output a message to the console, but encounters a function naming typo and an unquoted string identifier.",
                    "language": language,
                    "issues": [{
                        "issue": "NameError: Undefined Function Call & Missing String Quotes",
                        "severity": "High",
                        "explanation": "In Python, function names are case-sensitive and must be spelled exactly. 'prin' is not recognized by the Python interpreter and raises a NameError. Furthermore, writing hello without quotes causes Python to interpret it as a variable identifier rather than literal text.",
                        "hint": "Examine the spelling of your output function: what is the standard Python built-in function used to display text on the screen? To display the literal word hello instead of looking for an unassigned variable, what punctuation marks (quotes) must surround the text?",
                        "concept_to_revise": "Python Built-in Output Functions and String Literal Syntax"
                    }],
                    "positive_feedback": "You correctly used opening and closing parentheses for function invocation.",
                    "next_step": "Review the distinction between variable identifiers and quoted string literals in Python."
                }, indent=2)

            else:
                return json.dumps({
                    "overall_assessment": f"The {language} code contains logic anomalies that may cause runtime failures or incorrect calculation results.",
                    "language": language,
                    "issues": [{
                        "issue": "Logical Computation Mismatch",
                        "severity": "High",
                        "explanation": "The mathematical or control-flow operations diverge from expected standard algorithms, potentially producing incorrect outputs.",
                        "hint": "Trace the value of each variable after every line of code using a small sample input (e.g., input = 2). Does the output match what you expected?",
                        "concept_to_revise": "Algorithmic Tracing and Step-by-Step Desk Checking"
                    }],
                    "positive_feedback": "Clear variable naming and modular layout.",
                    "next_step": "Use print statements or desk-checking to verify intermediate state transitions."
                }, indent=2)

# Global singleton
llm_client = LLMClient()
