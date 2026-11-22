/**
 * Curated beginner code examples for CodeSense AI
 * Covering syntax, runtime, logical, and edge cases.
 */
const CODE_EXAMPLES = [
    {
        id: "py_syntax",
        title: "Python: Syntax Error (Missing Colon)",
        language: "Python",
        description: "Student tries to calculate a discounted price but forgets the colon in the function definition header.",
        code: `def calculate_discount(price, discount_rate)
    final_price = price - (price * discount_rate)
    return final_price

print(calculate_discount(150, 0.2))`
    },
    {
        id: "py_div_zero",
        title: "Python: Runtime Error (ZeroDivisionError)",
        language: "Python",
        description: "Calculate average score without checking if the total number of students is zero.",
        code: `total_marks = 450
student_count = int(input("Enter number of students: ")) # If user enters 0

class_average = total_marks / student_count
print("Average score is:", class_average)`
    },
    {
        id: "cpp_off_by_one",
        title: "C++: Runtime / Logic Error (Off-by-One Array Boundary)",
        language: "C++",
        description: "Iterating an array of 5 integers using <= 5, causing out-of-bounds access.",
        code: `#include <iostream>

int main() {
    int scores[5] = {85, 92, 78, 90, 88};
    
    // Loop tries to access scores[5] which is beyond allocated memory
    for (int i = 0; i <= 5; i++) {
        std::cout << "Score " << i << ": " << scores[i] << std::endl;
    }
    return 0;
}`
    },
    {
        id: "cpp_uninitialized",
        title: "C++: Logic Error (Uninitialized Variable)",
        language: "C++",
        description: "Using an uninitialized accumulator variable inside a summation loop.",
        code: `#include <iostream>

int main() {
    int sum; // Uninitialized garbage value!
    for (int i = 1; i <= 10; i++) {
        sum = sum + i;
    }
    std::cout << "Sum from 1 to 10: " << sum << std::endl;
    return 0;
}`
    },
    {
        id: "java_bounds",
        title: "Java: Runtime Error (ArrayIndexOutOfBoundsException)",
        language: "Java",
        description: "Accessing an invalid array index in a fixed-size array.",
        code: `public class TestGrades {
    public static void main(String[] args) {
        int[] grades = new int[5];
        grades[0] = 90;
        grades[1] = 85;
        grades[2] = 77;
        grades[3] = 95;
        grades[4] = 88;
        
        // Bug: Accessing index 5 in array of length 5
        System.out.println("Sixth student grade: " + grades[5]);
    }
}`
    },
    {
        id: "java_recursion",
        title: "Java: StackOverflowError (Missing Base Case)",
        language: "Java",
        description: "Recursive factorial function missing the base case when n <= 1.",
        code: `public class Factorial {
    public static int factorial(int n) {
        // Missing base case: if (n <= 1) return 1;
        return n * factorial(n - 1);
    }

    public static void main(String[] args) {
        System.out.println("Factorial of 5: " + factorial(5));
    }
}`
    },
    {
        id: "py_correct",
        title: "Python: Correct Program (Addition & Multiplication)",
        language: "Python",
        description: "A clean, working Python function with good variable names.",
        code: `def add(a, b):
    """Returns the arithmetic sum of two numbers."""
    return a + b

def multiply(a, b):
    """Returns the arithmetic product of two numbers."""
    return a * b

x = 10
y = 20
print("Sum is:", add(x, y))
print("Product is:", multiply(x, y))`
    },
    {
        id: "java_correct",
        title: "Java: Correct Clean Program",
        language: "Java",
        description: "A clean, well-formatted Java class computing area of a rectangle.",
        code: `public class RectangleArea {
    public static void main(String[] args) {
        int length = 12;
        int width = 8;
        int area = length * width;
        System.out.println("The area of the rectangle is: " + area);
    }
}`
    }
];
