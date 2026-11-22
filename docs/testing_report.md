# CodeSense AI – Comprehensive Testing & Validation Report
**Course:** Prompt Engineering (SCSE4041) | **Milestone:** Milestone 2  
**Project ID:** C4 | **Project Title:** Code Review Assistant for Beginner Programmers  
**Author:** Student Development Team | **Date:** November 2026  

---

## 1. Executive Testing Summary

The verification and validation framework for **CodeSense AI** comprises automated unit testing, end-to-end API integration testing, prompt formatting validation, response parsing robustness, and five live demonstration verification scenarios.

- **Test Framework:** `pytest 9.2.0` on Python 3.14 virtual environment
- **Total Test Cases Executed:** 26 automated tests + 5 live demonstration scenarios
- **Passed:** 26 (100%)
- **Failed / Skipped:** 0
- **Total Execution Duration:** 0.27 seconds

---

## 2. Test Suite Breakdown

### 2.1 Backend API Integration (`tests/test_api.py`)
| Test ID | Endpoint & Method | Purpose | Result |
|---|---|---|:---:|
| `API-01` | `GET /api/health` | Verifies service health, active provider detection, and supported languages | **PASSED** |
| `API-02` | `GET /` | Verifies web dashboard HTML rendering | **PASSED** |
| `API-03` | `GET /api/prompts` | Verifies metadata listing for P1, P2, and P3 | **PASSED** |
| `API-04` | `GET /api/prompts/P3` | Verifies template text retrieval for Final Optimized Prompt | **PASSED** |
| `API-05` | `POST /api/analyze` | Verifies end-to-end Python code review execution | **PASSED** |
| `API-06` | `POST /api/analyze` | Verifies HTTP 422 rejection on empty code submission | **PASSED** |
| `API-07` | `POST /api/analyze` | Verifies HTTP 422 rejection on unsupported languages (e.g. Bash/Rust) | **PASSED** |
| `API-08` | `POST /api/compare` | Verifies parallel multi-prompt matrix execution (P1 vs P2 vs P3) | **PASSED** |
| `API-09` | `GET/DELETE /api/history` | Verifies session history storage and clearing | **PASSED** |
| `API-10` | `POST /api/export-report` | Verifies Markdown report generation and download | **PASSED** |
| `API-11` | `POST /api/export-report` | Verifies PDF binary generation via ReportLab | **PASSED** |

### 2.2 Prompt Manager (`tests/test_prompt_manager.py`)
| Test ID | Component | Purpose | Result |
|---|---|---|:---:|
| `PM-01` | Cache Loader | Verifies all prompt templates (P1, P2, P3) exist and are loaded | **PASSED** |
| `PM-02` | Content Verification | Checks for pedagogical keywords ("SOCRATIC", "ANTI-LEAKAGE", "ROLE") | **PASSED** |
| `PM-03` | Variable Injection | Ensures `{language}`, `{code}`, `{context_block}` are replaced cleanly | **PASSED** |
| `PM-04` | Error Handling | Ensures `KeyError` is raised on non-existent prompt versions (e.g., P99) | **PASSED** |

### 2.3 Response Parser (`tests/test_response_parser.py`)
| Test ID | Component | Purpose | Result |
|---|---|---|:---:|
| `RP-01` | Markdown Stripper | Extracts valid JSON from triple-backtick markdown blocks | **PASSED** |
| `RP-02` | JSON Repair | Fixes trailing commas and invalid null/boolean constants | **PASSED** |
| `RP-03` | Schema Parsing | Parses model output into validated Pydantic `CodeAnalysisResponse` | **PASSED** |
| `RP-04` | Unstructured Normalizer | Gracefully normalizes free-form text from P1 into schema structure | **PASSED** |

### 2.4 Input & Schema Validation (`tests/test_validation.py`)
| Test ID | Component | Purpose | Result |
|---|---|---|:---:|
| `VAL-01` | `CodeAnalysisRequest` | Validates standard request model parsing | **PASSED** |
| `VAL-02` | Case Normalization | Normalizes language strings (e.g., 'cpp' -> 'C++', 'JAVA' -> 'Java') | **PASSED** |
| `VAL-03` | Language Whitelist | Rejects unsupported programming languages with clear error message | **PASSED** |
| `VAL-04` | Empty Code Guard | Rejects blank or whitespace-only code strings | **PASSED** |
| `VAL-05` | Version Whitelist | Enforces prompt version to be one of ['P1', 'P2', 'P3'] | **PASSED** |
| `VAL-06` | `CodeIssue` Model | Validates issue fields, severity types, and Socratic hints | **PASSED** |
| `VAL-07` | `CodeAnalysisResponse` | Validates empty issue handling for clean code submissions | **PASSED** |

---

## 3. Five Live Demonstration Scenarios

### Scenario 1: Python Syntax Error (Missing Colon)
- **Target Language:** Python
- **Input Code:**
  ```python
  def calculate_discount(price, discount_rate)
      final_price = price - (price * discount_rate)
      return final_price

  print(calculate_discount(150, 0.2))
  ```
- **Expected Finding:** SyntaxError: Missing colon `:` at end of function header line. Severity: Critical.
- **Actual CodeSense AI Output:**
  - *Overall Assessment:* "The program has a lexical syntax error that halts Python's parser before execution can begin."
  - *Detected Issue:* "SyntaxError: Missing Colon in Header Statement"
  - *Severity:* `Critical`
  - *Socratic Hint:* "Look closely at the very end of your function or loop header line. What punctuation mark does Python use to introduce an indented body of code?"
  - *Positive Feedback:* "You chose clear, self-explanatory parameter names and correctly intended to return a computed value."
  - *Zero Leakage:* Verified (no completed code block returned).
- **Result:** **PASSED**

---

### Scenario 2: Python Runtime Crash (ZeroDivisionError)
- **Target Language:** Python
- **Input Code:**
  ```python
  total_marks = 450
  student_count = int(input("Enter number of students: "))
  class_average = total_marks / student_count
  print("Average score is:", class_average)
  ```
- **Expected Finding:** Unhandled ZeroDivisionError when `student_count` is 0. Severity: High.
- **Actual CodeSense AI Output:**
  - *Overall Assessment:* "The code performs arithmetic operations correctly under typical conditions, but is vulnerable to an unhandled runtime crash when the denominator evaluates to zero."
  - *Detected Issue:* "Unhandled ZeroDivisionError (Division by Zero)"
  - *Severity:* `High`
  - *Socratic Hint:* "What conditional construct (`if`) could you place before the division to check whether your denominator is zero, and what fallback value or warning should be displayed?"
  - *Positive Feedback:* "Correct use of arithmetic division and sensible variable naming."
  - *Zero Leakage:* Verified.
- **Result:** **PASSED**

---

### Scenario 3: C++ Off-by-One Array Index Breach
- **Target Language:** C++
- **Input Code:**
  ```cpp
  #include <iostream>
  int main() {
      int scores[5] = {85, 92, 78, 90, 88};
      for (int i = 0; i <= 5; i++) {
          std::cout << "Score " << i << ": " << scores[i] << std::endl;
      }
      return 0;
  }
  ```
- **Expected Finding:** Off-by-one array out of bounds: loop condition `i <= 5` reads invalid index 5. Severity: Critical.
- **Actual CodeSense AI Output:**
  - *Overall Assessment:* "The program initializes an array and attempts iteration, but the loop condition breaches the allocated memory boundaries of the array."
  - *Detected Issue:* "Array Index Out of Bounds (Off-by-One Loop Error)"
  - *Severity:* `Critical`
  - *Socratic Hint:* "If an array has 5 elements, what is the index of the first element? What is the index of the last element? Does your loop condition (`<=`) allow the index counter to step one position too far?"
  - *Positive Feedback:* "Proper array initialization and clean iteration framework."
  - *Zero Leakage:* Verified.
- **Result:** **PASSED**

---

### Scenario 4: Java Missing Recursive Base Case (Infinite Recursion)
- **Target Language:** Java
- **Input Code:**
  ```java
  public class Factorial {
      public static int factorial(int n) {
          return n * factorial(n - 1);
      }
      public static void main(String[] args) {
          System.out.println(factorial(5));
      }
  }
  ```
- **Expected Finding:** Infinite recursion leading to StackOverflowError due to missing base condition. Severity: Critical.
- **Actual CodeSense AI Output:**
  - *Overall Assessment:* "The recursive function lacks an accessible base case, causing unlimited recursive calls that result in a stack overflow."
  - *Detected Issue:* "Missing Recursive Base Case (Infinite Recursion)"
  - *Severity:* `Critical`
  - *Socratic Hint:* "What is the simplest input for which this function should know the answer immediately without further calculation (e.g., when n is 0 or 1)? How can you return that early?"
  - *Positive Feedback:* "Good understanding of the mathematical recurrence relation."
  - *Zero Leakage:* Verified.
- **Result:** **PASSED**

---

### Scenario 5: Clean & Correct Java Program
- **Target Language:** Java
- **Input Code:**
  ```java
  public class RectangleArea {
      public static void main(String[] args) {
          int length = 12;
          int width = 8;
          int area = length * width;
          System.out.println("The area of the rectangle is: " + area);
      }
  }
  ```
- **Expected Finding:** Clean, working program. No errors detected. Severity: No issue detected.
- **Actual CodeSense AI Output:**
  - *Overall Assessment:* "Outstanding effort! Your Java program compiles cleanly, executes without runtime defects, and adheres to good programming conventions."
  - *Detected Issues:* None (empty array `[]`).
  - *Positive Feedback:* "Proper class definition, accurate `public static void main` signature, correct variable types, and clean string concatenation."
  - *Recommended Next Step:* "Consider exploring modular functions and defensive input boundary checks to deepen your software engineering skills."
- **Result:** **PASSED**

---

## 4. Verification Conclusion

CodeSense AI satisfies all technical, architectural, and pedagogical requirements for Milestone 2. Automated testing confirms 100% compliance across API contracts, validation guards, and schema parsers, while live demonstration scenarios prove robust error diagnosis and 0% complete-solution leakage.
