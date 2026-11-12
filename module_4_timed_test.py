# Module 4: Timed Test Engine
# Generates practice test questions from uploaded files and Error Notebook

import sys
import os
import ast
import random

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import module_3_logic_quiz as quiz


def build_available_question_bank(dir_path: str, errors: list, c: str) -> tuple:
    """Combines questions from uploaded files, Error Notebook, and general code logic."""
    q_list = []
    up_cnt = 0
    err_cnt = 0
    code_cnt = 0
    file_names = []

    # 1. Questions from files in user_files/
    if os.path.exists(dir_path):
        for f in os.listdir(dir_path):
            if f.endswith(".py"):
                file_names.append(f)
                fpath = os.path.join(dir_path, f)
                try:
                    with open(fpath, "r", encoding="utf-8") as file:
                        src = file.read()
                    t = ast.parse(src)
                    fns = [n.name for n in ast.walk(t) if isinstance(n, ast.FunctionDef)]
                    fn = fns[0] if fns else f.replace(".py", "")

                    q1 = quiz.build_shuffled_question(
                        q_text=f'In "{f}" (function "{fn}"), what happens if None is passed as an argument?',
                        correct_ans='It crashes with TypeError unless guarded with "if param is None: return 0"',
                        wrong_1="Python automatically treats None as the integer 0",
                        wrong_2="The function is skipped by Python without doing anything",
                        exp=f'In "{f}", operations on variables raise TypeError if None is passed without checking first.'
                    )
                    q1["source"] = f"Uploaded File ({f})"
                    q_list.append(q1)
                    up_cnt += 1

                    q2 = quiz.build_shuffled_question(
                        q_text=f'In "{fn}", why wrap computations in a try-except block?',
                        correct_ans="To safely catch runtime errors and return a fallback default (like 0)",
                        wrong_1="Because try-except blocks make CPU execution 2x faster",
                        wrong_2="Because Python requires all functions to have try blocks",
                        exp="Try-except stops uncaught errors so the rest of the application doesn't crash."
                    )
                    q2["source"] = f"Uploaded File ({f})"
                    q_list.append(q2)
                    up_cnt += 1

                    has_loop = any(isinstance(n, (ast.For, ast.While)) for n in ast.walk(t))
                    if has_loop:
                        q3 = quiz.build_shuffled_question(
                            q_text=f'In "{f}", what happens if a loop index goes past the end of a list?',
                            correct_ans="IndexError occurs because the list does not have that index",
                            wrong_1="The operating system shuts down Python",
                            wrong_2="Python expands the list in memory automatically",
                            exp="Accessing an index past len(list) raises IndexError."
                        )
                        q3["source"] = f"Uploaded File ({f})"
                        q_list.append(q3)
                        up_cnt += 1
                except Exception:
                    pass

    # 2. Questions from Error Notebook
    for err in errors:
        q_err = quiz.get_error_quiz_data(err)
        q_err["source"] = f"Error Notebook ({err.get('func', 'error')})"
        q_list.append(q_err)
        err_cnt += 1

        fn_name = err.get("func", "routine")
        err_type = err.get("type", "Runtime Error")
        q_err2 = quiz.build_shuffled_question(
            q_text=f'For the crash recorded in your Error Notebook for "{fn_name}" ({err_type}), how should it be handled?',
            correct_ans="Wrap the block in try-except and return a safe default value (0 or False)",
            wrong_1="Catch it with bare except: pass and leave variables unassigned",
            wrong_2="Repeat the function call until the CPU resolves it",
            exp=f"Catching {err_type} and returning a safe fallback value prevents the program from aborting."
        )
        q_err2["source"] = f"Error Notebook ({fn_name})"
        q_list.append(q_err2)
        err_cnt += 1

    # 3. Questions from active code AST
    q_mut1 = quiz.get_mutant_quiz_data(c, 1)
    q_mut1["source"] = "Code Boundaries"
    q_list.append(q_mut1)
    code_cnt += 1

    q_mut2 = quiz.get_mutant_quiz_data(c, 2)
    q_mut2["source"] = "Type Checking"
    q_list.append(q_mut2)
    code_cnt += 1

    q_mut3 = quiz.get_mutant_quiz_data(c, 3)
    q_mut3["source"] = "Edge Invariants"
    q_list.append(q_mut3)
    code_cnt += 1

    # 4. Standard Python core invariants
    basics = [
        quiz.build_shuffled_question(
            q_text="In Python list operations, what happens when accessing arr[0] on an empty list []?",
            correct_ans="IndexError is raised because the list contains zero elements",
            wrong_1="Python automatically returns None without raising an error",
            wrong_2="The list automatically appends a 0 at index 0",
            exp='Empty lists have length 0. Always check "if not arr: return 0" before indexing.'
        ),
        quiz.build_shuffled_question(
            q_text='In division, what check should precede "a / b" to avoid crashing?',
            correct_ans='Checking "if b == 0: return 0" to defend against ZeroDivisionError',
            wrong_1='Checking "if a == b: return 0"',
            wrong_2="Division by zero never raises an exception in standard Python",
            exp="Dividing by zero raises ZeroDivisionError. Checking denominator avoids the crash."
        ),
        quiz.build_shuffled_question(
            q_text="Why check negative numbers before running a while loop that counts down?",
            correct_ans="To guarantee the loop stops and does not run infinitely",
            wrong_1="Because negative numbers delete files",
            wrong_2="Because while loops only accept positive numbers in Python",
            exp="Counting down from a negative number when expecting positive values can cause infinite loops."
        ),
        quiz.build_shuffled_question(
            q_text="What happens when accessing a missing key in a dictionary data[key]?",
            correct_ans="KeyError is raised; use data.get(key, default) to handle it safely",
            wrong_1="IndexError is raised",
            wrong_2="Dictionaries never fail when accessing missing keys in Python",
            exp='Using data.get(key, 0) safely returns a fallback without raising KeyError.'
        )
    ]
    for b in basics:
        b["source"] = "Python Invariants"
        q_list.append(b)
        code_cnt += 1

    info = {
        "total": len(q_list),
        "uploaded_count": up_cnt,
        "error_count": err_cnt,
        "code_count": code_cnt,
        "uploaded_names": file_names
    }

    return q_list, info


def generate_comprehensive_timed_test(dir_path: str, errors: list, c: str, count: int = 3) -> list:
    """Randomly samples questions from the question bank."""
    bank, _ = build_available_question_bank(dir_path, errors, c)
    random.shuffle(bank)
    return bank[:count]


def inspect_available_pool(dir_path: str, errors: list, c: str):
    """Prints breakdown of available questions."""
    pool, info = build_available_question_bank(dir_path, errors, c)
    print("Available questions:")
    print(f"  Total           : {info['total']}")
    print(f"  Uploaded scripts: {info['uploaded_count']} ({len(info['uploaded_names'])} files)")
    print(f"  Error Notebook  : {info['error_count']}")
    print(f"  Code logic      : {info['code_count']}")
    return pool, info


def run_cli_timed_test(dir_path: str, errors: list, c: str, count: int = 3, per_q_sec: int = 15):
    """Terminal timed test simulation."""
    pool, _ = inspect_available_pool(dir_path, errors, c)
    random.shuffle(pool)
    chosen = pool[:min(count, len(pool))]

    print(f"\nStarting test ({len(chosen)} questions, {per_q_sec}s per question)...\n")
    score = 0
    records = []

    for i, item in enumerate(chosen, 1):
        print(f"Question {i} of {len(chosen)}: {item['question']}")
        for opt in item["options"]:
            print(f"  ({opt['key']}) {opt['text']}")

        k = item["correct"]
        print(f"  Selected: Option ({k})")
        score += 1
        records.append({"num": i, "q": item["question"], "ans": k, "exp": item["explanation"]})

    print("-" * 40)
    print(f"Test Complete! Score: {score}/{len(chosen)} (100%)")
    print("-" * 40)
    return score, records


if __name__ == "__main__":
    print("Python Mentor: Module 4 (Timed Test)")
    print("-" * 40)

    base = os.path.dirname(__file__)
    uf = os.path.join(base, "user_files")
    dummy_err = [{"func": "factorial", "type": "TypeError", "reason": "None input"}]
    dummy_c = "def factorial(n):\n    return 1\n"

    run_cli_timed_test(uf, dummy_err, dummy_c, count=3, per_q_sec=15)
