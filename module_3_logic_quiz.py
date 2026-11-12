# Module 3: Logic Quiz Generator
# Generates multiple-choice questions to test understanding of code and edge cases

import sys
import os
import re
import ast
import random

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def build_shuffled_question(q_text: str, correct_ans: str, wrong_1: str, wrong_2: str, exp: str) -> dict:
    """Randomly shuffles options so the correct answer is not always Option A."""
    pool = [
        {"text": correct_ans, "is_correct": True},
        {"text": wrong_1, "is_correct": False},
        {"text": wrong_2, "is_correct": False}
    ]
    random.shuffle(pool)

    keys = ["A", "B", "C"]
    opts = []
    corr_key = "A"

    for i, item in enumerate(pool):
        k = keys[i]
        opts.append({"key": k, "text": item["text"]})
        if item["is_correct"]:
            corr_key = k

    return {
        "question": q_text,
        "options": opts,
        "correct": corr_key,
        "explanation": exp
    }


def get_mutant_quiz_data(c: str, q_num: int = 1) -> dict:
    """Generates logic questions based on function AST."""
    has_lt = "<" in c
    has_rng = "range(" in c
    is_rec = False

    try:
        t = ast.parse(c)
        for n in ast.walk(t):
            if isinstance(n, ast.FunctionDef):
                fn = n.name
                for child in ast.walk(n):
                    if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and child.func.id == fn:
                        is_rec = True
    except Exception:
        pass

    # Question 1: Loop and condition limits
    if q_num == 1:
        if has_lt or has_rng:
            return build_shuffled_question(
                q_text='If we change the loop condition "<" to "<=", how does the code behave?',
                correct_ans="The loop runs one extra iteration for the boundary value",
                wrong_1="The loop stops on the very first iteration",
                wrong_2="The result stays exactly the same",
                exp='Changing "<" to "<=" includes the upper value, so the loop executes one additional time.'
            )
        else:
            return build_shuffled_question(
                q_text="What happens if this function is called with input 0?",
                correct_ans="It handles 0 as a base case and returns a valid result",
                wrong_1="It crashes with UnboundLocalError immediately",
                wrong_2="It enters an infinite loop that never stops",
                exp="Zero (0) is a common boundary value. Safe code handles 0 as a base case rather than failing."
            )

    # Question 2: Input checking
    elif q_num == 2:
        return build_shuffled_question(
            q_text='Why is adding "if n is None: return 0" at the start a good practice?',
            correct_ans="It stops TypeError crashes before doing math or list operations",
            wrong_1="It forces the compiler to run twice as fast",
            wrong_2="It is just a comment that Python ignores",
            exp='In Python, operations like n + 1 crash with TypeError if n is None. Checking "if n is None: return 0" prevents this.'
        )

    # Question 3: Negative numbers or recursion
    else:
        if is_rec:
            return build_shuffled_question(
                q_text="In recursive code, what happens if negative inputs are not checked?",
                correct_ans="RecursionError occurs because the base case is never reached",
                wrong_1="Python automatically converts negative numbers to positive",
                wrong_2="It finishes normally and returns None",
                exp="Recursive calls decrement toward 0. Negative numbers keep decrementing until stack depth runs out."
            )
        else:
            return build_shuffled_question(
                q_text="What happens if a negative number (like -5) is passed without validation?",
                correct_ans="Loop ranges or conditions may run 0 times and return unexpected values",
                wrong_1="The computer automatically deletes the file",
                wrong_2="Python syntax does not allow negative numbers in functions",
                exp="Passing unvalidated negative numbers can cause range(1, -4) to loop 0 times, giving wrong results."
            )


def get_error_quiz_data(err_entry: dict) -> dict:
    """Generates a question from a recorded error in Error Notebook."""
    fn = err_entry.get("func", "your function")
    err_type = err_entry.get("type", "TypeError")
    reason = err_entry.get("reason", "empty input")

    return build_shuffled_question(
        q_text=f'Earlier, "{fn}" failed with "{err_type}" on "{reason}". How should this be fixed in Python?',
        correct_ans=f'Add an input check "if param is None: return 0" at the start of "{fn}"',
        wrong_1="Leave the code as-is and hope callers only pass valid data",
        wrong_2="Delete the entire function and start over",
        exp=f'When a function crashes with {err_type} on {reason}, check inputs at the entry of the function to handle it safely.'
    )


def grade_viva(user_ans: str, exp_corr: str = "A", exp_text: str = ""):
    """Checks student's answer and returns (is_correct, explanation)."""
    s = user_ans.strip().lower()
    exp = exp_corr.lower()

    m = re.search(r'\boption\s*([abc])\b|^\(([abc])\)|^([abc])[\):\s]', s)
    if m:
        chosen = (m.group(1) or m.group(2) or m.group(3)).lower()
        return (chosen == exp), exp_text

    if s in ["a", "b", "c"]:
        return (s == exp), exp_text

    ok = False
    if f"({exp})" in s or f"option {exp}" in s or s.startswith(exp):
        ok = True

    return ok, exp_text


def run_cli_quiz_session(c: str, total_q: int = 3):
    """Terminal quiz demo."""
    score = 0
    for i in range(1, total_q + 1):
        q = get_mutant_quiz_data(c, i)
        print(f"\nQuestion {i} of {total_q}:")
        print(q["question"])
        for opt in q["options"]:
            print(f"  ({opt['key']}) {opt['text']}")
        print(f"Correct answer: ({q['correct']})")
        print(f"Explanation: {q['explanation']}")
        score += 1
    print(f"\nQuiz completed. Score: {score}/{total_q}")


if __name__ == "__main__":
    print("Python Mentor: Module 3 (Logic Quiz)")
    print("-" * 40)

    sample = """def factorial(n):
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res
"""
    print("Sample code:\n" + sample)
    run_cli_quiz_session(sample, 3)
