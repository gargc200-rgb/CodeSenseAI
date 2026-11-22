# CodeSense AI – Demonstration Test Scenarios
**Course:** Prompt Engineering (SCSE4041) | **Milestone:** Milestone 2  

This document provides five repeatable demonstration scenarios that evaluators or presenters can execute to observe CodeSense AI in action.

---

## Scenario 1: Python Syntax Error (Missing Colon)
- **Language:** Python
- **Bug Category:** Syntax Error
- **Input Code:**
  ```python
  def calculate_discount(price, discount_rate)
      final_price = price - (price * discount_rate)
      return final_price

  print(calculate_discount(150, 0.2))
  ```
- **Context:** Student tries to write a function calculating price after discount, but forgets the colon on line 1.
- **Expected Finding:** Lexical SyntaxError halting parser. Severity: `Critical`.
- **Expected Socratic Hint:** Asks student what character is required at the end of a `def` header line in Python.
- **Leakage Check:** No complete code block returned.

---

## Scenario 2: Python Division by Zero (Runtime Crash)
- **Language:** Python
- **Bug Category:** Fatal Runtime Exception
- **Input Code:**
  ```python
  total_marks = 450
  student_count = int(input("Enter number of students: ")) # e.g. 0
  class_average = total_marks / student_count
  print("Average score is:", class_average)
  ```
- **Context:** Calculating class average without defensive guard when student count is 0.
- **Expected Finding:** ZeroDivisionError. Severity: `High`.
- **Expected Socratic Hint:** Inquires how an `if` statement can validate the divisor before performing mathematical division.
- **Leakage Check:** 0% code leaked.

---

## Scenario 3: C++ Array Index Out of Bounds (Off-by-One)
- **Language:** C++
- **Bug Category:** Memory Breach / Undefined Behavior
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
- **Context:** Loop iterates with `i <= 5` on an array of length 5, reading beyond allocated stack memory.
- **Expected Finding:** Array boundary exceeded. Severity: `Critical`.
- **Expected Socratic Hint:** Questions whether an array of size 5 has a legal index 5, and prompts checking the termination condition (`<` vs `<=`).
- **Leakage Check:** Zero code leaked.

---

## Scenario 4: Java Missing Recursive Base Case (Stack Overflow)
- **Language:** Java
- **Bug Category:** Unbounded Recursion
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
- **Context:** Recursive factorial function missing the termination condition when `n <= 1`.
- **Expected Finding:** StackOverflowError. Severity: `Critical`.
- **Expected Socratic Hint:** Asks what is the simplest input where the function should return an answer immediately without recursing.
- **Leakage Check:** Zero code leaked.

---

## Scenario 5: Clean & Correct Java Program
- **Language:** Java
- **Bug Category:** Control / Clean Code
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
- **Context:** Syntactically and logically clean Java program computing rectangle area.
- **Expected Finding:** No issues detected. Severity: `No issue detected`.
- **Expected Positive Feedback:** Praises class structure, main signature, and clean variable typing.
- **Expected Next Step:** Encourages user input via `Scanner` or writing separate methods.
- **Leakage Check:** Zero code leaked.
