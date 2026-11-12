# Python Mentor: Python Code Tester & Practice Tool

Python Mentor is a Python project built to test functions against common edge cases (like 0, None, negative numbers, and empty lists), automatically patch crashes, and generate practice quizzes.

---

## 👥 5-Member Team Modules

Each team member has a dedicated module file and test runner:

| Member | Module File | Test Runner | Responsibility |
| :--- | :--- | :--- | :--- |
| **Member 1** | `module_1_test_code.py` | `test_module_1.bat` | **Test Code:** Runs functions with edge-case inputs (None, 0, -1, empty lists) |
| **Member 2** | `module_2_fix_code.py` | `test_module_2.bat` | **Fix Code:** Adds safety checks and try-except blocks to stop crashes |
| **Member 3** | `module_3_logic_quiz.py` | `test_module_3.bat` | **Logic Quiz:** Multiple-choice questions on code logic and loop limits |
| **Member 4** | `module_4_timed_test.py` | `test_module_4.bat` | **Timed Test:** Practice tests with per-question timers |
| **Member 5** | `module_5_error_notebook.py` | `test_module_5.bat` | **Error Notebook:** Records crashes, lets user delete entries or clear all |

**Project Lead:**
- `app.py`: Web interface (Streamlit) uniting all 5 modules.
- `run.bat`: Launches the web application.

---

## 🚀 How to Run

### 1. Run the Full Web Application
Double-click `run.bat` or run in terminal:
```bash
streamlit run app.py
```
Open browser at `http://localhost:8501`.

### 2. Run Individual Modules (Terminal)
Double-click any member's `.bat` file to run in terminal:
- `test_module_1.bat` -> Runs edge-case test demo
- `test_module_2.bat` -> Runs code fixer demo
- `test_module_3.bat` -> Runs logic quiz demo
- `test_module_4.bat` -> Runs timed test demo
- `test_module_5.bat` -> Runs error notebook demo

---

## 📌 Features
- **Pure Python:** Uses Python standard library (`ast`, `subprocess`, `difflib`, `random`, `json`).
- **No API Keys:** Runs completely locally without third-party cloud services.
- **Persistent Error Log:** Error Notebook persists across sessions so you don't lose error history.
