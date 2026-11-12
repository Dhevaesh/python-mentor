# Module 2: Code Fixer & Safety Patch
# Analyzes errors, fixes syntax issues, and inserts defensive guards + try-except blocks

import sys
import os
import ast
import difflib
import subprocess

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import module_1_test_code as tester


def generate_code_diff(orig: str, fixed: str) -> str:
    """Generates simple diff between original and fixed code."""
    d = difflib.unified_diff(
        orig.strip().splitlines(),
        fixed.strip().splitlines(),
        fromfile="original.py",
        tofile="fixed.py",
        lineterm=""
    )
    return "\n".join(d)


def unwrap_outer_try_except(code: str) -> str:
    """Strips accidental or unwanted outer try...except Exception: pass wrappers."""
    lines = code.splitlines()
    if not lines:
        return code

    first_idx = -1
    for i, l in enumerate(lines):
        if l.strip():
            first_idx = i
            break
    if first_idx == -1:
        return code

    last_idx = -1
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip():
            last_idx = i
            break

    if lines[first_idx].strip() == "try:":
        except_idx = -1
        for i in range(last_idx, first_idx, -1):
            if lines[i].strip().startswith("except"):
                except_idx = i
                break

        if except_idx > first_idx:
            tail_lines = [lines[k].strip() for k in range(except_idx + 1, last_idx + 1) if lines[k].strip()]
            if not tail_lines or any(w in tail_lines[0] for w in ["pass", "return", "continue"]):
                body_lines = lines[first_idx + 1:except_idx]
                cleaned = []
                for bl in body_lines:
                    if bl.startswith("    "):
                        cleaned.append(bl[4:])
                    elif bl.startswith("\t"):
                        cleaned.append(bl[1:])
                    else:
                        cleaned.append(bl)
                return "\n".join(cleaned)
    return code


def repair_syntax_errors(code: str) -> tuple:
    """Detects and fixes syntax errors like missing colons or single '=' in if-conditions."""
    try:
        ast.parse(code)
        return code, False, ""
    except SyntaxError as e:
        err_msg = str(e.msg)
        lineno = e.lineno
        lines = code.splitlines()

        if lineno is not None and 1 <= lineno <= len(lines):
            bad_line = lines[lineno - 1]
            stripped = bad_line.strip()

            # 1. Missing colon at end of control statements
            control_keywords = ["def ", "if ", "elif ", "else", "for ", "while ", "try", "except", "finally", "class ", "with "]
            for kw in control_keywords:
                if (stripped.startswith(kw) or stripped == kw.strip()) and not stripped.endswith(":"):
                    lines[lineno - 1] = bad_line + ":"
                    fixed_code = "\n".join(lines)
                    try:
                        ast.parse(fixed_code)
                        return fixed_code, True, f"Added missing ':' at line {lineno}."
                    except SyntaxError:
                        pass

            # 2. Single '=' in if/elif statement
            if stripped.startswith("if ") or stripped.startswith("elif "):
                if " = " in bad_line and " == " not in bad_line and " <= " not in bad_line and " >= " not in bad_line and " != " not in bad_line:
                    lines[lineno - 1] = bad_line.replace(" = ", " == ", 1)
                    fixed_code = "\n".join(lines)
                    try:
                        ast.parse(fixed_code)
                        return fixed_code, True, f"Replaced assignment '=' with comparison '==' at line {lineno}."
                    except SyntaxError:
                        pass

        return code, False, f"SyntaxError at line {lineno}: {err_msg}"


def heal_function_with_try_except(code: str, err_trace: str) -> str:
    """Adds defensive guard check and wraps body in try-except block."""
    lines = code.splitlines()
    def_idx = -1
    for i, l in enumerate(lines):
        if l.strip().startswith("def ") and ":" in l:
            def_idx = i
            break

    if def_idx == -1:
        # Script without def
        if lines and lines[0].strip() == "try:" and any("except" in l for l in lines):
            return code
        indented = ["    " + l if l.strip() else "" for l in lines]
        return "try:\n" + "\n".join(indented) + "\nexcept Exception as e:\n    print(f'Runtime error: {e}')"

    fn_line = lines[def_idx]
    try:
        t = ast.parse(code)
        fn_node = [n for n in ast.walk(t) if isinstance(n, ast.FunctionDef)][0]
        params = [a.arg for a in fn_node.args.args if a.arg != "self"]
        fn_name = fn_node.name
    except Exception:
        params = ["n"]
        fn_name = "function"

    p0 = params[0] if params else "n"
    is_math = any(k in fn_name.lower() or k in code.lower() for k in ["factorial", "fibonacci", "power", "gcd", "lcm", "sum"])

    if "ZeroDivision" in err_trace or "division by zero" in err_trace:
        den = params[-1] if len(params) > 1 else p0
        guard = f"if {den} == 0: return 0"
    elif "IndexError" in err_trace:
        guard = f"if not {p0}: return 0"
    elif is_math:
        guard = f"if {p0} is None or {p0} < 0: return 0"
    else:
        guard = f"if {p0} is None: return 0"

    body_lines = lines[def_idx + 1:]
    doc_lines = []
    rest_body = body_lines
    if body_lines and (body_lines[0].strip().startswith('"""') or body_lines[0].strip().startswith("'''")):
        quote = body_lines[0].strip()[:3]
        if body_lines[0].strip().count(quote) >= 2 and len(body_lines[0].strip()) > 3:
            doc_lines = [body_lines[0]]
            rest_body = body_lines[1:]
        else:
            for k in range(len(body_lines)):
                doc_lines.append(body_lines[k])
                if k > 0 and quote in body_lines[k]:
                    rest_body = body_lines[k + 1:]
                    break

    cleaned_rest = []
    in_try = False
    for bl in rest_body:
        s = bl.strip()
        if s.startswith("if ") and ("is None" in s or "< 0" in s or "== 0" in s or "not " in s) and "return" in s:
            continue
        if s == "try:":
            in_try = True
            continue
        if s.startswith("except ") or s == "except:":
            in_try = False
            continue
        if not in_try:
            cleaned_rest.append(bl)
        else:
            if bl.startswith("        "):
                cleaned_rest.append("    " + bl[8:])
            elif bl.startswith("    \t"):
                cleaned_rest.append("    " + bl[5:])
            else:
                cleaned_rest.append(bl)

    result = [fn_line]
    for dl in doc_lines:
        result.append(dl)
    result.append("    " + guard)
    result.append("    try:")
    for rb in cleaned_rest:
        if rb.strip():
            base = rb.strip()
            indent_level = len(rb) - len(rb.lstrip())
            new_indent = " " * max(8, indent_level + 4)
            result.append(new_indent + base)
        else:
            result.append("")
    result.append("    except Exception:")
    result.append("        return 0")

    return "\n".join(result)


def check_script_execution(code: str) -> tuple:
    """Runs a script in an isolated subprocess to test if it executes cleanly."""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=3
        )
        if proc.returncode == 0:
            return True, proc.stdout.strip()
        else:
            return False, proc.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "Script timed out (> 3s). Possible infinite loop."
    except Exception as e:
        return False, str(e)


def analyze_error(c: str, err: str) -> dict:
    """Explains why the code crashed and how it is fixed."""
    info = tester.inspect_function_details(c)
    fn = info.get("func_name") or "script"
    p = info.get("params", [])

    s = str(err)

    if not s or "NO_FUNCTION_FOUND" in s or "ALL_PASSED" in s:
        return {
            "function": fn,
            "vulnerability": "Unhandled Boundary Exceptions",
            "root_cause": "Function lacked explicit defensive guards and try-except error handling.",
            "remediation": "Added input boundary check and wrapped execution body in try-except block.",
            "raw_error": ""
        }

    if "SyntaxError" in s:
        prob = "Syntax Error"
        cause = f"Python parser encountered invalid syntax: {s[:70]}."
        fix = "Corrected syntax error so code can execute."
    elif "NoneType" in s or "'<=' not supported" in s or "unsupported operand" in s:
        prob = "Missing check for None input"
        cause = f"The function `{fn}` operated on parameter {p} without verifying if it was None."
        fix = f'Added "if {p[0] if p else "n"} is None: return 0" guard and wrapped body in try-except.'
    elif "ZeroDivision" in s or "division by zero" in s:
        prob = "Division by zero"
        cause = "The code divided a number by zero on boundary input."
        fix = "Added zero division guard and wrapped body in try-except."
    elif "IndexError" in s:
        prob = "Index out of range"
        cause = "The code accessed an index outside collection boundaries."
        fix = "Added length validation check and wrapped body in try-except."
    elif "Timeout" in s or "timed out" in s:
        prob = "Infinite Loop or Recursion"
        cause = "The loop or recursion did not reach a termination condition."
        fix = "Added boundary check and try-except safety block."
    else:
        prob = "Runtime Exception"
        cause = f"The code crashed during execution: {s[:70]}."
        fix = "Added defensive input check and wrapped execution in try-except block."

    return {
        "function": fn,
        "vulnerability": prob,
        "root_cause": cause,
        "remediation": fix,
        "raw_error": s[:100]
    }


def repair_code(broken_code: str, err_trace: str):
    """Repairs code and returns (fixed_code, note, diff_str, analysis)."""
    # 1. Strip any accidental outer try...except pass wrappers if double wrapped
    cleaned_code = unwrap_outer_try_except(broken_code)

    # 2. Check and fix syntax errors
    syntax_fixed, was_syntax_repaired, syntax_note = repair_syntax_errors(cleaned_code)
    if was_syntax_repaired:
        analysis = {
            "function": "syntax",
            "vulnerability": "Syntax Error",
            "root_cause": syntax_note,
            "remediation": "Fixed syntax error so code can execute.",
            "raw_error": syntax_note
        }
        diff_str = generate_code_diff(broken_code, syntax_fixed)
        return syntax_fixed, syntax_note, diff_str, analysis

    # 3. Always apply defensive guard + try-except block
    fixed_code = heal_function_with_try_except(syntax_fixed, err_trace)
    analysis = analyze_error(broken_code, err_trace)
    note = f"Added defensive input checks and try-except block to {analysis['function']}."
    diff_str = generate_code_diff(broken_code, fixed_code)

    return fixed_code, note, diff_str, analysis


def repair_and_analyze(c: str, err: str = ""):
    """Terminal helper to analyze error and show fixed code."""
    fixed, note, diff_str, analysis = repair_code(c, err)
    print("Function   :", analysis["function"])
    print("Status     :", analysis["vulnerability"])
    print("Cause      :", analysis["root_cause"])
    print("Fix        :", analysis["remediation"])

    print("\nChanges:")
    print(diff_str if diff_str else "(No changes)")
    print("\nFixed code:\n" + fixed)
    return fixed, analysis


if __name__ == "__main__":
    print("Python Mentor: Module 2 (Code Fixer)")
    print("-" * 40)

    sample = """def factorial(n):
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res
"""
    err = "TypeError: '<=' not supported between instances of 'int' and 'NoneType'"

    print("Original code:\n" + sample)
    print("Error:", err)
    print("\nFixing code...\n")
    repair_and_analyze(sample, err)
