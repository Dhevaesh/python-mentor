# Module 5: Error Notebook
# Records runtime errors, classifies them, and lets user delete or clear them

import sys
import os

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


class ErrorNotebook:
    """Manages recorded runtime errors."""
    def __init__(self):
        self.notebook = []

    def classify_error(self, fn: str, err: str, val):
        """Classifies raw runtime exception into simple categories."""
        if "NoneType" in err:
            err_type = "TypeError (None input)"
            reason = "Crashed when given an empty None input"
        elif "ZeroDivision" in err:
            err_type = "ZeroDivisionError"
            reason = "Division by zero on 0 input"
        elif "IndexError" in err:
            err_type = "IndexError"
            reason = "List index out of range on empty list []"
        elif "RecursionError" in err:
            err_type = "RecursionError"
            reason = "Recursion depth exceeded"
        else:
            err_type = "Runtime Error"
            reason = f"Crashed on input {val}"

        # Prevent duplicate entries
        for item in self.notebook:
            if item["func"] == fn and item["type"] == err_type:
                return item

        record = {
            "func": fn or "code",
            "type": err_type,
            "reason": reason,
            "raw": err[:100]
        }
        self.notebook.append(record)
        return record

    def delete_error(self, idx: int):
        """Removes a specific error record by index."""
        if 0 <= idx < len(self.notebook):
            return self.notebook.pop(idx)
        return None

    def clear_all(self):
        """Clears all logged failures."""
        self.notebook.clear()

    def display_bulletin(self):
        """Prints recorded errors in terminal."""
        print("Error Notebook:")
        if not self.notebook:
            print("  Notebook is clean! No errors recorded.")
            return

        for i, item in enumerate(self.notebook, 1):
            print(f"  [{i}] {item['func']} - {item['type']}")
            print(f"      Cause: {item['reason']}")
            print(f"      Trace: {item['raw']}")


if __name__ == "__main__":
    print("Python Mentor: Module 5 (Error Notebook)")
    print("-" * 40)

    nb = ErrorNotebook()
    nb.classify_error("divide", "ZeroDivisionError: division by zero", [0, 0])
    nb.classify_error("factorial", "TypeError: '<=' not supported between int and NoneType", None)
    nb.classify_error("first_elem", "IndexError: list index out of range", [])

    nb.display_bulletin()

    print("\nDeleting entry 2 (factorial)...")
    nb.delete_error(1)
    nb.display_bulletin()
