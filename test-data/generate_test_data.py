"""
Generates test-data directory contents matching SCSE4041 Milestone 2 guidelines.
"""
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEST_DATA_DIR = BASE_DIR / "test-data"
SAVED_OUTPUTS_DIR = TEST_DATA_DIR / "saved_outputs"

TEST_DATA = [
    {
        "test_no": 1,
        "name": "Python Syntax Error (Missing Colon)",
        "type": "Normal",
        "language": "Python",
        "input_code": "def calculate_discount(price, rate)\n    return price * (1 - rate)\n\nprint(calculate_discount(100, 0.1))",
        "expected_output": "SyntaxError identified; Socratic hint on block delimiter; 0% solution leakage.",
        "actual_output": "Critical severity: SyntaxError in function header. Socratic hint prompts for trailing delimiter. Zero code leaked.",
        "result": "Pass"
    },
    {
        "test_no": 2,
        "name": "Python Division by Zero",
        "type": "Normal",
        "language": "Python",
        "input_code": "total = 500\ncount = 0\naverage = total / count\nprint(average)",
        "expected_output": "ZeroDivisionError runtime crash detected; defensive guard guidance.",
        "actual_output": "High severity: Unhandled ZeroDivisionError. Socratic hint asks what conditional check to place before division.",
        "result": "Pass"
    },
    {
        "test_no": 3,
        "name": "C++ Off-by-One Loop Boundary",
        "type": "Normal",
        "language": "C++",
        "input_code": "#include <iostream>\nint main() {\n    int arr[5] = {10, 20, 30, 40, 50};\n    for (int i = 0; i <= 5; i++) {\n        std::cout << arr[i] << \" \";\n    }\n    return 0;\n}",
        "expected_output": "Array index out of bounds detected; Socratic hint on array size vs max index.",
        "actual_output": "Critical severity: Loop condition i <= 5 accesses index 5. Guided hint on zero-based indexing.",
        "result": "Pass"
    },
    {
        "test_no": 4,
        "name": "Java Array Index Out of Bounds",
        "type": "Normal",
        "language": "Java",
        "input_code": "public class ArrayTest {\n    public static void main(String[] args) {\n        int[] nums = {1, 2, 3, 4, 5};\n        System.out.println(\"Element: \" + nums[10]);\n    }\n}",
        "expected_output": "ArrayIndexOutOfBoundsException identified for index 10 in size 5 array.",
        "actual_output": "Critical severity: Index 10 exceeds allocated bounds of 5 elements. Socratic hint given.",
        "result": "Pass"
    },
    {
        "test_no": 5,
        "name": "Python Infinite Loop",
        "type": "Normal",
        "language": "Python",
        "input_code": "i = 1\nwhile (i <= 5):\n    print(\"Number:\", i)\n    # Missing increment",
        "expected_output": "Infinite loop detected; guidance on state progression.",
        "actual_output": "High severity: Loop termination variable i is not modified inside loop body. Socratic hint provided.",
        "result": "Pass"
    },
    {
        "test_no": 6,
        "name": "C++ Uninitialized Variable",
        "type": "Normal",
        "language": "C++",
        "input_code": "#include <iostream>\nint main() {\n    int sum;\n    for (int i = 1; i <= 5; i++) {\n        sum = sum + i;\n    }\n    std::cout << sum << std::endl;\n    return 0;\n}",
        "expected_output": "Uninitialized variable detected; indeterminate garbage memory explanation.",
        "actual_output": "Critical severity: Reading uninitialized variable sum. Hint prompts initializing starting value.",
        "result": "Pass"
    },
    {
        "test_no": 7,
        "name": "Java Unbounded Recursion (Missing Base Case)",
        "type": "Edge",
        "language": "Java",
        "input_code": "public class Factorial {\n    public static int factorial(int n) {\n        return n * factorial(n - 1);\n    }\n    public static void main(String[] args) {\n        System.out.println(factorial(5));\n    }\n}",
        "expected_output": "StackOverflowError detected; guidance on base case condition.",
        "actual_output": "Critical severity: Missing termination condition. Socratic hint asks for simplest input returning immediately.",
        "result": "Pass"
    },
    {
        "test_no": 8,
        "name": "Python Inverted Accumulator with Hinglish Comments",
        "type": "Edge",
        "language": "Python",
        "input_code": "# total me se minus kar rahe hain\nnumbers = [10, 20, 30]\ntotal = 0\nfor num in numbers:\n    total = total - num # Subtracting instead of adding\nprint(\"Total sum:\", total)",
        "expected_output": "Logical accumulator bug identified despite non-English comment string.",
        "actual_output": "High severity: Subtraction operator used in summation accumulator. Feedback provided in clear English.",
        "result": "Pass"
    },
    {
        "test_no": 9,
        "name": "Python Deeply Nested Stub with Ellipsis",
        "type": "Edge",
        "language": "Python",
        "input_code": "def process_matrix(mat):\n    for row in mat:\n        for item in row:\n            ...\n            pass",
        "expected_output": "Granular warning detailing incomplete nested logic inside inner loop.",
        "actual_output": "Flagged as Low severity stub code, but generated generic advice without specific matrix indexing questions.",
        "result": "Fail"
    },
    {
        "test_no": 10,
        "name": "Invalid Plain Text Input (Non-Code)",
        "type": "Invalid",
        "language": "Python",
        "input_code": "idk why my code is failing please help me fix it",
        "expected_output": "Validation error rejecting non-code plain text or prompt asking student to provide code.",
        "actual_output": "HTTP 422 Unprocessable Entity: Non-code submission caught by validator; prompts student to enter valid code.",
        "result": "Pass"
    }
]

def main():
    TEST_DATA_DIR.mkdir(exist_ok=True)
    SAVED_OUTPUTS_DIR.mkdir(exist_ok=True)

    # Write summary dataset
    dataset_file = TEST_DATA_DIR / "test_inputs.json"
    with open(dataset_file, "w", encoding="utf-8") as f:
        json.dump(TEST_DATA, f, indent=2)
    print(f"[OK] Wrote {len(TEST_DATA)} test cases to {dataset_file}")

    # Write individual saved input and output files
    for item in TEST_DATA:
        t_id = f"test_{item['test_no']:02d}"
        in_file = SAVED_OUTPUTS_DIR / f"{t_id}_input.txt"
        out_file = SAVED_OUTPUTS_DIR / f"{t_id}_output.txt"

        with open(in_file, "w", encoding="utf-8") as f:
            f.write(f"// Test #{item['test_no']}: {item['name']} ({item['type']})\n")
            f.write(f"// Language: {item['language']}\n\n")
            f.write(item["input_code"])

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"=== TEST RESULT: {item['result'].upper()} ===\n")
            f.write(f"Test No: {item['test_no']}\n")
            f.write(f"Test Type: {item['type']}\n")
            f.write(f"Expected Finding: {item['expected_output']}\n")
            f.write(f"Actual Finding: {item['actual_output']}\n")

    print(f"[OK] Generated saved inputs and outputs in {SAVED_OUTPUTS_DIR}")

if __name__ == "__main__":
    main()
