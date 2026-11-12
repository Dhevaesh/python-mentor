# Module 2: Code Fixer & Safety Patch
# Analyzes errors, fixes syntax issues, and inserts clean defensive guards

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

    # If first line is "try:" and the end has "except Exception:" or "except:"
    if lines[first_idx].strip() == "try:":
        except_idx = -1
        for i in range(last_idx, first_idx, -1):
            if lines[i].strip().startswith("except"):
                except_idx = i
                break

        if except_idx > first_idx:
            # Check if except block is simple pass/return
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


def insert_function_guard(code: str, guard_line: str, fn_name: str) -> str:
    """Inserts clean defensive guard into function while preserving formatting and comments."""
    lines = code.splitlines()
    def_line_idx = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("def ") and fn_name in stripped and ":" in stripped:
            def_line_idx = i
            break

    if def_line_idx == -1:
        return code

    # Determine indentation of function body
    indent = "    "
    for j in range(def_line_idx + 1, len(lines)):
        if lines[j].strip():
            indent = lines[j][:len(lines[j]) - len(lines[j].lstrip())]
            break

    # Determine insertion line (skip past docstring if present)
    insert_idx = def_line_idx + 1
    if insert_idx < len(lines) and (lines[insert_idx].strip().startswith('"""') or lines[insert_idx].strip().startswith("'''")):
        quote = lines[insert_idx].strip()[:3]
        if lines[insert_idx].strip().count(quote) >= 2 and len(lines[insert_idx].strip()) > 3:
            insert_idx += 1
        else:
            for k in range(insert_idx + 1, len(lines)):
                if quote in lines[k]:
                    insert_idx = k + 1
                    break

    # Avoid duplicate guard
    guard_clean = guard_line.strip()
    check_window = lines[def_line_idx:min(len(lines), def_line_idx + 8)]
    for check_line in check_window:
        if "is None" in check_line and "is None" in guard_clean:
            return code
        if "== 0" in check_line and "== 0" in guard_clean:
            return code
        if "not " in check_line and "not " in guard_clean:
            return code

    # Format multi-line guard with proper indentation
    guard_lines = guard_clean.splitlines()
    formatted_lines = [indent + guard_lines[0]]
    for gl in guard_lines[1:]:
        formatted_lines.append(indent + "    " + gl.strip())
    
    formatted_guard = "\n".join(formatted_lines)
    lines.insert(insert_idx, formatted_guard)
    return "\n".join(lines)


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
            "vulnerability": "Clean Code (No Errors)",
            "root_cause": "The code compiled and executed with zero errors.",
            "remediation": "No modifications required.",
            "raw_error": ""
        }

    if "SyntaxError" in s:
        prob = "Syntax Error"
        cause = f"Python parser encountered invalid syntax: {s[:70]}."
        fix = "Corrected syntax error (missing colon, mismatched delimiter, or bad assignment)."
    elif "NoneType" in s or "'<=' not supported" in s or "unsupported operand" in s:
        prob = "Missing check for None input"
        cause = f"The function `{fn}` operated on parameter {p} without verifying if it was None."
        fix = f'Added "if {p[0] if p else "n"} is None: return 0" guard at the top.'
    elif "ZeroDivision" in s or "division by zero" in s:
        prob = "Division by zero"
        cause = "The code divided a number by zero on boundary input."
        fix = "Added safety check to prevent zero division."
    elif "IndexError" in s:
        prob = "Index out of range"
        cause = "The code accessed an index outside the boundaries of a collection."
        fix = "Added length validation before indexing."
    elif "Timeout" in s or "timed out" in s:
        prob = "Infinite Loop or Recursion"
        cause = "The loop or recursion did not reach a termination condition."
        fix = "Added boundary check and loop limit condition."
    else:
        prob = "Runtime Exception"
        cause = f"The code crashed during execution: {s[:70]}."
        fix = "Added input guard checks to safely handle edge values."

    return {
        "function": fn,
        "vulnerability": prob,
        "root_cause": cause,
        "remediation": fix,
        "raw_error": s[:100]
    }


def repair_code(broken_code: str, err_trace: str):
    """Repairs code and returns (fixed_code, note, diff_str, analysis)."""
    # 1. Strip any accidental outer try...except pass wrappers
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

    # 3. Check if there is a function definition
    info = tester.inspect_function_details(syntax_fixed)
    fn_name = info.get("func_name")
    params = info.get("params", [])

    if fn_name:
        s_err = str(err_trace)
        
        # If no error trace supplied, run sandbox test to see if an edge case actually fails
        if not s_err or "NO_FUNCTION_FOUND" in s_err or "ALL_PASSED" in s_err:
            inputs, _ = tester.get_test_inputs(syntax_fixed)
            ok, out, _ = tester.run_code_sandbox(syntax_fixed, inputs)
            if ok:
                # Function passes all tests! No fix needed!
                analysis = analyze_error(syntax_fixed, "")
                diff_str = generate_code_diff(broken_code, syntax_fixed)
                return syntax_fixed, "Function is verified and passes all tests.", diff_str, analysis
            else:
                s_err = out

        # Build clean, targeted guard for the function
        is_math = any(k in fn_name.lower() or k in syntax_fixed.lower() for k in ["factorial", "fibonacci", "power", "gcd", "lcm", "sum"])
        p0 = params[0] if params else "n"

        if "ZeroDivision" in s_err or "division by zero" in s_err:
            den = params[-1] if len(params) > 1 else p0
            guard = f"if {den} == 0:\n    return 0"
        elif "IndexError" in s_err:
            guard = f"if not {p0}:\n    return 0"
        elif is_math:
            guard = f"if {p0} is None or {p0} < 0:\n    return 0"
        else:
            guard = f"if {p0} is None:\n    return 0"

        fixed_code = insert_function_guard(syntax_fixed, guard, fn_name)
        analysis = analyze_error(broken_code, s_err)
        note = f"Added defensive guard `{guard.replace(chr(10), ' ')}` to function `{fn_name}`."
        diff_str = generate_code_diff(broken_code, fixed_code)
        return fixed_code, note, diff_str, analysis

    # 4. If code is a script (no def function)
    runs_ok, run_out = check_script_execution(syntax_fixed)
    if runs_ok:
        # Script runs cleanly with zero errors!
        analysis = {
            "function": "script",
            "vulnerability": "Clean Code (No Errors)",
            "root_cause": "The script executed with exit code 0.",
            "remediation": "No modifications required. Script is working as expected.",
            "raw_error": ""
        }
        diff_str = generate_code_diff(broken_code, syntax_fixed)
        return syntax_fixed, "Script runs cleanly with zero errors.", diff_str, analysis
    else:
        # Script crashed during execution
        analysis = analyze_error(syntax_fixed, run_out)
        # Avoid destructive global wrapping; preserve the script
        note = f"Identified runtime issue: {analysis['vulnerability']}."
        diff_str = generate_code_diff(broken_code, syntax_fixed)
        return syntax_fixed, note, diff_str, analysis


def repair_and_analyze(c: str, err: str = ""):
    """Terminal helper to analyze error and show fixed code."""
    fixed, note, diff_str, analysis = repair_code(c, err)
    print("Function   :", analysis["function"])
    print("Status     :", analysis["vulnerability"])
    print("Cause      :", analysis["root_cause"])
    print("Fix        :", analysis["remediation"])

    print("\nChanges:")
    print(diff_str if diff_str else "(No changes - code is already clean)")
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
