# Module 1: Code Tester & Edge Case Checker
# Tests functions with edge cases (None, 0, negative numbers, empty lists)

import sys
import os
import ast
import time
import subprocess

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def inspect_function_details(c: str) -> dict:
    """Gets function name and parameter list from source code."""
    try:
        t = ast.parse(c)
        for n in ast.walk(t):
            if isinstance(n, ast.FunctionDef):
                p = [a.arg for a in n.args.args if a.arg != "self"]
                return {
                    "func_name": n.name,
                    "params": p,
                    "num_params": len(p),
                    "line_count": len(c.splitlines())
                }
    except Exception:
        pass
    return {"func_name": None, "params": [], "num_params": 0, "line_count": len(c.splitlines())}


def infer_param_types(p: list) -> list:
    """Guesses parameter types based on variable name."""
    t = []
    for x in p:
        s = x.lower()
        if any(k in s for k in ["nums", "arr", "list", "items", "elements", "lst", "matrix"]):
            t.append("list")
        elif any(k in s for k in ["name", "text", "str", "word", "char", "line"]):
            t.append("str")
        elif any(k in s for k in ["dict", "mapping", "map", "data", "record", "config"]):
            t.append("dict")
        else:
            t.append("num")
    return t


def get_test_inputs(c: str):
    """Builds test inputs with common edge cases."""
    d = inspect_function_details(c)
    n = d["num_params"]
    p = d["params"]

    if n == 0:
        return [[] for _ in range(5)], "default"

    t = infer_param_types(p)
    cases = []
    vals = [
        {"num": 0, "str": "", "list": [], "dict": {}},
        {"num": -1, "str": "a", "list": [0], "dict": {"k": 0}},
        {"num": 100, "str": "test", "list": [1, -1, 0], "dict": {}},
        {"num": None, "str": None, "list": None, "dict": None},
        {"num": 999999, "str": "xyz", "list": [999999], "dict": {"a": 1}}
    ]

    for v in vals:
        row = [v[k] for k in t]
        cases.append(row if n > 1 else row[0])

    return cases, "edge-cases"


def run_code_sandbox(c: str, tests: list):
    """Runs the code in a subprocess to test if it crashes."""
    runner = f"""
import sys, inspect

if __name__ == '__main__':
    funcs = [v for k, v in list(locals().items()) if callable(v) and not k.startswith('__') and getattr(v, '__code__', None) and v.__code__.co_filename == '<string>']
    if not funcs:
        funcs = [v for k, v in list(locals().items()) if callable(v) and not k.startswith('__')]
    if not funcs:
        sys.exit(0)

    fn = funcs[0]
    n = len(inspect.signature(fn).parameters)
    tests = {repr(tests)}

    for i, x in enumerate(tests):
        try:
            if isinstance(x, (list, tuple)):
                a = list(x)
                if len(a) < n:
                    a += [0] * (n - len(a))
                elif len(a) > n:
                    a = a[:n]
                fn(*a)
            else:
                fn(*([x] * n)) if n > 1 else fn(x)
        except Exception as e:
            print(f"Failed on input {{i+1}} ({{x}}): {{type(e).__name__}} -> {{e}}", file=sys.stderr)
            raise
    print("ALL_PASSED")
"""
    code_to_run = c + "\n" + runner
    t0 = time.time()

    try:
        proc = subprocess.run(
            [sys.executable, "-c", code_to_run],
            capture_output=True,
            text=True,
            timeout=4
        )
        elapsed = round(time.time() - t0, 3)
        if proc.returncode == 0:
            return True, proc.stdout.strip(), elapsed
        else:
            return False, proc.stderr.strip(), elapsed
    except subprocess.TimeoutExpired:
        return False, "Code timed out (> 4s). Loop or recursion didn't terminate.", 4.0
    except Exception as e:
        return False, str(e), 0.0


def test_code_snippet(c: str):
    """Runs edge case tests and prints output."""
    d = inspect_function_details(c)
    fn_name = d.get("func_name") or "function"
    print(f"Testing function: {fn_name}")
    print(f"Parameters: {d.get('params', [])}")

    inputs, _ = get_test_inputs(c)
    print("\nTest inputs:")
    for i, inp in enumerate(inputs, 1):
        print(f"  Test {i}: {inp}")

    print("\nRunning tests...")
    ok, out, elapsed = run_code_sandbox(c, inputs)

    if ok:
        print(f"\nResult: PASS ({elapsed}s)")
        return True, out
    else:
        print(f"\nResult: FAIL ({elapsed}s)")
        print(f"Error output:\n{out.strip()}")
        return False, out


if __name__ == "__main__":
    print("Python Mentor: Module 1 (Code Tester)")
    print("-" * 40)

    sample = """def divide(a, b):
    return a / b
"""
    print("Sample code:\n" + sample)
    test_code_snippet(sample)
