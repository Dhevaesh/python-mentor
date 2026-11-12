import os
import ast
import json
import time
import random
import importlib
import streamlit as st
import streamlit.components.v1 as components
import module_1_test_code as tester
import module_2_fix_code as healer
import module_3_logic_quiz as quiz_engine
import module_4_timed_test as timed_engine
import module_5_error_notebook as notebook_engine

# Map quiz and timed test modules
viva = quiz_engine
viva.build_available_question_bank = timed_engine.build_available_question_bank
viva.generate_comprehensive_timed_test = timed_engine.generate_comprehensive_timed_test

# Guarantee hot-reloading of modules on every rerun
importlib.reload(tester)
importlib.reload(healer)
importlib.reload(quiz_engine)
importlib.reload(timed_engine)
importlib.reload(notebook_engine)

# -------------------------------------------------------------
# 1. PAGE CONFIG & MODERN ACADEMIC DEVELOPER THEME (100% PURE PYTHON)
# -------------------------------------------------------------
BOT_AVATAR_PATH = os.path.join(os.path.dirname(__file__), "assets", "bot_avatar.png")
USER_AVATAR_PATH = os.path.join(os.path.dirname(__file__), "assets", "user_avatar.png")

st.set_page_config(
    page_title="Python Mentor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Clean GitHub Dark / JetBrains Academic Theme */
    .stApp {
        background: #0d1117;
        color: #e6edf3;
    }
    
    /* Professional Developer Title */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #f0f6fc !important;
        letter-spacing: -0.02em;
        margin: 0 0 2px 0;
        line-height: 1.2;
    }
    .main-title .accent {
        color: #10b981 !important;
    }
    
    .sub-title {
        font-size: 0.92rem;
        color: #8b949e;
        margin-bottom: 16px;
    }

    /* Engine Status Badge (Green/Active) */
    .status-badge-green {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(16, 185, 129, 0.12);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    /* Clean Developer Chat Message Bubble */
    .stChatMessage {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
    }

    /* Clean Circular Terminal & User Avatars */
    div[data-testid="stChatMessageAvatar"] {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 50% !important;
        overflow: hidden !important;
        width: 38px !important;
        height: 38px !important;
    }
    div[data-testid="stChatMessageAvatar"] img {
        border-radius: 50% !important;
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
    }
    
    pre, code {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Sidebar Section Headings (Muted Slate) */
    .sidebar-heading {
        color: #8b949e !important;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 14px;
        margin-bottom: 6px;
        letter-spacing: 0.05em;
    }

    /* Clean Developer Action Buttons */
    div[data-testid="stHorizontalBlock"] button {
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.86rem !important;
        border: 1px solid #30363d !important;
        background: #21262d !important;
        color: #f0f6fc !important;
        transition: all 0.15s ease;
    }
    div[data-testid="stHorizontalBlock"] button:hover {
        background: #30363d !important;
        border-color: #8b949e !important;
        color: #ffffff !important;
    }

    /* Interactive Quiz Box */
    .interactive-quiz-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 12px 0 14px 0;
    }
    .interactive-quiz-header {
        font-size: 0.82rem;
        font-weight: 700;
        color: #10b981;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .interactive-quiz-question {
        font-size: 1.05rem;
        font-weight: 600;
        color: #f0f6fc;
        margin-bottom: 4px;
    }

    /* Clean Dark Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid #21262d !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# -------------------------------------------------------------
# 2. WELCOME MESSAGE: CLEAN DEVELOPER CAPABILITIES
# -------------------------------------------------------------
def get_welcome_message():
    return {
        "role": "assistant",
        "content": (
            "<div style='font-size: 1.15rem; font-weight: 800; color: #10b981; margin-bottom: 4px;'>"
            "Python Mentor: Python Learning & Practice Tool</div>\n\n"
            "<div style='color: #8b949e; font-size: 0.92rem; margin-bottom: 14px;'>"
            "Test functions with edge cases (like 0, None, negative numbers), automatically fix crashes, and take practice quizzes.</div>\n\n"
            "<div style='font-size: 0.8rem; font-weight: 700; color: #8b949e; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;'>"
            "Features:</div>\n\n"
            "<div style='display: flex; flex-direction: column; gap: 8px;'>\n"
            "  <div style='background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 10px 14px;'>\n"
            "    <b style='color: #10b981;'>⚡ Test Code</b><br>\n"
            "    <span style='color: #8b949e; font-size: 0.88rem;'>Runs edge cases (None, 0, negative numbers, empty lists) to check for crashes.</span>\n"
            "  </div>\n"
            "  <div style='background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 10px 14px;'>\n"
            "    <b style='color: #10b981;'>🛡️ Fix Code</b><br>\n"
            "    <span style='color: #8b949e; font-size: 0.88rem;'>Adds input checks and try-except blocks so the code runs safely.</span>\n"
            "  </div>\n"
            "  <div style='background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 10px 14px;'>\n"
            "    <b style='color: #10b981;'>🎯 Logic Quiz</b><br>\n"
            "    <span style='color: #8b949e; font-size: 0.88rem;'>Questions on loop boundaries, conditions, and recursion logic.</span>\n"
            "  </div>\n"
            "  <div style='background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 10px 14px;'>\n"
            "    <b style='color: #10b981;'>⏱️ Timed Test</b><br>\n"
            "    <span style='color: #8b949e; font-size: 0.88rem;'>Short practice test with a timer based on your files and past errors.</span>\n"
            "  </div>\n"
            "  <div style='background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 10px 14px;'>\n"
            "    <b style='color: #10b981;'>📓 Error Notebook</b><br>\n"
            "    <span style='color: #8b949e; font-size: 0.88rem;'>Review past errors, delete items, or practice fixing them.</span>\n"
            "  </div>\n"
            "</div>"
        )
    }

# -------------------------------------------------------------
# 3. STATE INITIALIZATION
# -------------------------------------------------------------
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [get_welcome_message()]
else:
    first_msg = st.session_state.messages[0].get("content", "")
    if "PYTHON MENTOR" not in first_msg.upper():
        st.session_state.messages[0] = get_welcome_message()

if "current_code" not in st.session_state:
    st.session_state.current_code = "def factorial(n):\n    res = 1\n    for i in range(1, n + 1):\n        res *= i\n    return res\n"

ERROR_NOTEBOOK_FILE = os.path.join(os.path.dirname(__file__), "user_files", "error_notebook.json")

def load_error_notebook_from_disk() -> list:
    if os.path.exists(ERROR_NOTEBOOK_FILE):
        try:
            with open(ERROR_NOTEBOOK_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []

def save_error_notebook_to_disk(errors: list):
    try:
        os.makedirs(os.path.dirname(ERROR_NOTEBOOK_FILE), exist_ok=True)
        with open(ERROR_NOTEBOOK_FILE, "w", encoding="utf-8") as f:
            json.dump(errors, f, indent=2)
    except Exception:
        pass

if "last_error" not in st.session_state:
    st.session_state.last_error = ""
if "healed_code" not in st.session_state:
    st.session_state.healed_code = ""
if "error_notebook" not in st.session_state:
    st.session_state.error_notebook = load_error_notebook_from_disk()
if "active_file_path" not in st.session_state:
    st.session_state.active_file_path = os.path.join(os.path.dirname(__file__), "user_files", "sample.py")

# Quiz & Re-practice State Management
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False
if "quiz_question_num" not in st.session_state:
    st.session_state.quiz_question_num = 1
if "current_quiz_data" not in st.session_state:
    st.session_state.current_quiz_data = None
if "quiz_missed_questions" not in st.session_state:
    st.session_state.quiz_missed_questions = []
if "asking_quiz_retry" not in st.session_state:
    st.session_state.asking_quiz_retry = False
if "asking_quiz_permission" not in st.session_state:
    st.session_state.asking_quiz_permission = False
if "asking_error_quiz_permission" not in st.session_state:
    st.session_state.asking_error_quiz_permission = False
if "error_quiz_active" not in st.session_state:
    st.session_state.error_quiz_active = False

# Timed Test State Management
if "show_test_setup" not in st.session_state:
    st.session_state.show_test_setup = False
if "timed_test_active" not in st.session_state:
    st.session_state.timed_test_active = False
if "timed_test_start_time" not in st.session_state:
    st.session_state.timed_test_start_time = 0.0
if "timed_test_q_start_time" not in st.session_state:
    st.session_state.timed_test_q_start_time = 0.0
if "timed_test_q_num" not in st.session_state:
    st.session_state.timed_test_q_num = 1
if "timed_test_total_q" not in st.session_state:
    st.session_state.timed_test_total_q = 3
if "timed_test_per_q_limit" not in st.session_state:
    st.session_state.timed_test_per_q_limit = 15
if "timed_test_questions" not in st.session_state:
    st.session_state.timed_test_questions = []
if "timed_test_score" not in st.session_state:
    st.session_state.timed_test_score = 0
if "timed_test_missed" not in st.session_state:
    st.session_state.timed_test_missed = []
if "asking_test_retry" not in st.session_state:
    st.session_state.asking_test_retry = False

# -------------------------------------------------------------
# 4. SIDEBAR: CLEAN ACADEMIC CONTROLS
# -------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-heading">CONTROLS</div>', unsafe_allow_html=True)
    
    if st.button("New Session", use_container_width=True):
        st.session_state.messages = [get_welcome_message()]
        st.session_state.last_error = ""
        st.session_state.healed_code = ""
        st.session_state.quiz_active = False
        st.session_state.quiz_question_num = 1
        st.session_state.current_quiz_data = None
        st.session_state.quiz_missed_questions = []
        st.session_state.asking_quiz_retry = False
        st.session_state.asking_quiz_permission = False
        st.session_state.asking_error_quiz_permission = False
        st.session_state.error_quiz_active = False
        st.session_state.show_test_setup = False
        st.session_state.timed_test_active = False
        st.session_state.timed_test_questions = []
        st.session_state.timed_test_score = 0
        st.session_state.timed_test_missed = []
        st.session_state.asking_test_retry = False
        # Explicitly preserve Error Notebook data across sessions
        st.session_state.error_notebook = load_error_notebook_from_disk()
        st.rerun()

    st.divider()

    st.markdown('<div class="sidebar-heading">FILES & CODE</div>', unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader("Upload .py file", type=["py"])
    if uploaded_file and uploaded_file.name != st.session_state.get("last_uploaded_name"):
        upload_dir = os.path.join(os.path.dirname(__file__), "user_files")
        os.makedirs(upload_dir, exist_ok=True)
        custom_file_path = os.path.join(upload_dir, uploaded_file.name)
        
        with open(custom_file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        st.session_state.current_code = uploaded_file.getvalue().decode("utf-8")
        st.session_state.active_file_path = custom_file_path
        st.session_state.last_uploaded_name = uploaded_file.name
        st.session_state.last_error = ""

    # Error Notebook Drawer with Individual Delete Buttons
    nb_len = len(st.session_state.error_notebook)
    with st.expander(f"📓 Error Notebook ({nb_len})", expanded=False):
        if not st.session_state.error_notebook:
            st.caption("No failures recorded. Notebook is clean!")
        else:
            for s_idx, s_item in enumerate(st.session_state.error_notebook):
                c_desc, c_del = st.columns([4, 1])
                with c_desc:
                    st.markdown(f"<span style='font-size: 0.82rem;'><b>{s_item['func']}</b>: <code style='color: #f59e0b;'>{s_item['type']}</code></span>", unsafe_allow_html=True)
                with c_del:
                    if st.button("🗑️", key=f"sb_del_{s_idx}_{s_item.get('func', '')}", help=f"Delete error #{s_idx+1}", use_container_width=True):
                        st.session_state.error_notebook.pop(s_idx)
                        save_error_notebook_to_disk(st.session_state.error_notebook)
                        st.toast("✔ Error removed from notebook!")
                        st.rerun()
            if st.button("🗑️ Clear All", key="sb_clear_all_errors", use_container_width=True):
                st.session_state.error_notebook = []
                save_error_notebook_to_disk([])
                st.toast("✔ All errors cleared!")
                st.rerun()

    st.divider()

    # Code Editor
    st.markdown('<div class="sidebar-heading">SOURCE WORKSPACE</div>', unsafe_allow_html=True)
    func_info = tester.inspect_function_details(st.session_state.current_code)
    st.caption(f"Target: `{func_info['func_name'] or 'script'}` | Lines: {func_info['line_count']}")
    
    user_code = st.text_area("Source Code:", value=st.session_state.current_code, height=180, label_visibility="collapsed")
    st.session_state.current_code = user_code

# -------------------------------------------------------------
# 5. MAIN VIEW: PYTHON MENTOR (CLEAN STUDENT INTERFACE)
# -------------------------------------------------------------
st.markdown('<div class="main-title">Python Mentor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Python Code Testing, Auto-Repair & Practice Quizzes</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. TOP QUICK ACTIONS BAR (5 ACTIONS INCLUDING TIMED TEST)
# -------------------------------------------------------------
col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
btn_trigger = None

with col_b1:
    if st.button("⚡ Test Code", use_container_width=True):
        btn_trigger = "Test code"
with col_b2:
    if st.button("🛡️ Fix Code", use_container_width=True):
        btn_trigger = "Fix code"
with col_b3:
    if st.button("🎯 Logic Quiz", use_container_width=True):
        btn_trigger = "Start logic quiz"
with col_b4:
    if st.button("⏱️ Timed Test", use_container_width=True):
        st.session_state.show_test_setup = not st.session_state.show_test_setup
        st.rerun()
with col_b5:
    if st.button("📓 Error Notebook", use_container_width=True):
        btn_trigger = "Show error notebook"
        st.session_state.show_test_setup = False

# -------------------------------------------------------------
# 7B. TIMED TEST SETUP PANEL
# -------------------------------------------------------------
if st.session_state.show_test_setup and not st.session_state.timed_test_active:
    upload_dir = os.path.join(os.path.dirname(__file__), "user_files")
    pool_questions, breakdown = viva.build_available_question_bank(
        upload_dir, st.session_state.error_notebook, st.session_state.current_code
    )
    total_avail = breakdown["total"]
    up_cnt = breakdown["uploaded_count"]
    err_cnt = breakdown["error_count"]
    code_cnt = breakdown["code_count"]
    files_str = ", ".join(breakdown["uploaded_names"]) if breakdown["uploaded_names"] else "None uploaded"

    st.markdown("### ⏱️ Timed Test Setup")
    st.caption("Practice questions created from your uploaded Python files, past errors, and code logic.")

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("📁 Uploaded Files", f"{up_cnt} questions", help=files_str)
    col_m2.metric("📓 Error Notebook", f"{err_cnt} questions", help="From past test crashes")
    col_m3.metric("⚡ Logic Checks", f"{code_cnt} questions", help="Boundary conditions and edge cases")

    col_cfg1, col_cfg2 = st.columns(2)
    with col_cfg1:
        chosen_num_q = st.slider(
            "Number of Questions for Test:",
            min_value=1,
            max_value=max(1, total_avail),
            value=min(3, total_avail),
            step=1,
            key="cfg_exam_num_q"
        )
    with col_cfg2:
        chosen_per_q_time = st.slider(
            "Time Limit Per Question (seconds):",
            min_value=5,
            max_value=30,
            value=15,
            step=1,
            key="cfg_exam_time_limit",
            help="Per-question countdown: Minimum 5 seconds, Maximum 30 seconds."
        )

    col_btn1, col_btn2 = st.columns([2, 1])
    with col_btn1:
        if st.button("🚀 Start Test", key="btn_start_exam_configured", use_container_width=True):
            random.shuffle(pool_questions)
            selected_exam_q = pool_questions[:chosen_num_q]

            st.session_state.show_test_setup = False
            st.session_state.timed_test_active = True
            st.session_state.timed_test_questions = selected_exam_q
            st.session_state.timed_test_total_q = len(selected_exam_q)
            st.session_state.timed_test_q_num = 1
            st.session_state.timed_test_per_q_limit = chosen_per_q_time
            st.session_state.timed_test_q_start_time = time.time()
            st.session_state.timed_test_score = 0
            st.session_state.timed_test_answers = []
            st.session_state.timed_test_missed = []
            st.session_state.current_quiz_data = selected_exam_q[0]

            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    f"<div style='font-size: 1.1rem; font-weight: 700; color: #10b981; margin-bottom: 6px;'>⏱️ Timed Test Started ({len(selected_exam_q)} Questions)</div>\n\n"
                    f"• <b>Time Limit:</b> {chosen_per_q_time} seconds per question (Min 5s, Max 30s)<br>"
                    f"• <i>Questions are appearing in the interactive test card below. Results and explanations will be displayed at the end of the test.</i>"
                )
            })
            st.rerun()

    with col_btn2:
        if st.button("✕ Cancel Setup", key="btn_cancel_exam_config", use_container_width=True):
            st.session_state.show_test_setup = False
            st.rerun()

# -------------------------------------------------------------
# 8. HELPERS: NOTEBOOK & LOGGING
# -------------------------------------------------------------
def record_error_in_notebook(func_name: str, error_msg: str, input_val):
    if "NoneType" in error_msg:
        err_type = "TypeError (None input)"
        reason = "Crashed when passed an empty NoneType input"
    elif "ZeroDivision" in error_msg:
        err_type = "ZeroDivisionError"
        reason = "Division by zero on zero boundary"
    elif "IndexError" in error_msg:
        err_type = "IndexError"
        reason = "Accessing out-of-bounds index on empty collection []"
    else:
        err_type = "Runtime / Logic Error"
        reason = f"Crashed on test vector {input_val}"

    for item in st.session_state.error_notebook:
        if item["func"] == func_name and item["type"] == err_type:
            return

    st.session_state.error_notebook.append({
        "func": func_name or "code",
        "type": err_type,
        "reason": reason,
        "raw": error_msg[:100]
    })
    save_error_notebook_to_disk(st.session_state.error_notebook)

def format_error_notebook_bulletin() -> str:
    if not st.session_state.error_notebook:
        return (
            "<div style='background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 14px 18px; margin: 4px 0;'>"
            "<div style='font-size: 1.05rem; font-weight: 700; color: #10b981; margin-bottom: 6px;'>📓 Error Notebook</div>"
            "<span style='color: #8b949e;'>Your Error Notebook is clean! No errors recorded.</span>"
            "</div>"
        )

    res = (
        "<div style='background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 14px 18px; margin: 4px 0;'>"
        "<div style='font-size: 1.05rem; font-weight: 700; color: #10b981; margin-bottom: 10px;'>📓 Recorded Errors</div>"
    )
    for idx, item in enumerate(st.session_state.error_notebook, 1):
        res += (
            f"<div style='padding: 8px 0; border-bottom: 1px solid #21262d;'>"
            f"<b>[{idx}] Function:</b> <code style='color: #58a6ff;'>{item['func']}</code> | "
            f"<b>Error:</b> <span style='color: #f59e0b; font-weight: 600;'>{item['type']}</span><br>"
            f"<span style='color: #8b949e; font-size: 0.88rem; margin-left: 12px;'><i>Cause:</i> {item['reason']}</span><br>"
            f"<span style='color: #6e7681; font-size: 0.82rem; font-family: monospace; margin-left: 12px;'>Trace: {item.get('raw', '')[:80]}</span>"
            f"</div>"
        )
    res += "</div>"
    return res

# -------------------------------------------------------------
# 9. CHAT & ACTION DISPATCHER (WITH TIMED TEST & RE-ATTEMPT LOOP)
# -------------------------------------------------------------
def process_user_input(user_prompt: str):
    p = user_prompt.lower().strip()
    active_code = st.session_state.current_code

    # Check if user wants to stop the active quiz or test
    if st.session_state.quiz_active or st.session_state.error_quiz_active or st.session_state.timed_test_active:
        if any(w in p for w in ["stop", "exit", "quit", "dont want", "don't want", "enough", "later", "conclude", "finish"]):
            st.session_state.quiz_active = False
            st.session_state.error_quiz_active = False
            st.session_state.timed_test_active = False
            st.session_state.current_quiz_data = None
            st.session_state.quiz_question_num = 1
            st.session_state.asking_quiz_retry = False
            st.session_state.asking_test_retry = False
            return {
                "role": "assistant",
                "content": "<div style='font-size: 1rem; font-weight: 700; color: #10b981;'>Session Paused</div>\n\nYou can test code, fix errors, or review your <b style='color: #10b981;'>Error Notebook</b>."
            }

    # Handling User Answering Re-attempt Missed Questions Prompt
    if st.session_state.asking_quiz_retry:
        st.session_state.asking_quiz_retry = False
        if any(w in p for w in ["yes", "retry", "sure", "ok", "again", "practice"]):
            if st.session_state.quiz_missed_questions:
                st.session_state.quiz_active = True
                st.session_state.quiz_question_num = 1
                q_retry = st.session_state.quiz_missed_questions.pop(0)
                st.session_state.current_quiz_data = q_retry
                return {
                    "role": "assistant",
                    "content": (
                        f"<div style='font-size: 1.05rem; font-weight: 700; color: #f59e0b; margin-bottom: 6px;'>🔁 Retry Question:</div>\n\n"
                        f"<b>Question:</b> {q_retry['question']}"
                    )
                }
        else:
            st.session_state.quiz_missed_questions = []
            return {
                "role": "assistant",
                "content": "Quiz completed! You can test another code example anytime."
            }

    # Handling User Answering Post-Test Options: Retake Whole Test, Retake Missed Questions, Quit Test
    if st.session_state.asking_test_retry:
        st.session_state.asking_test_retry = False
        
        # 1. Retake Whole Test
        if any(w in p for w in ["whole", "retake whole", "all questions", "restart"]):
            st.session_state.timed_test_active = True
            upload_dir = os.path.join(os.path.dirname(__file__), "user_files")
            pool_q, _ = viva.build_available_question_bank(
                upload_dir, st.session_state.error_notebook, st.session_state.current_code
            )
            random.shuffle(pool_q)
            tot_q = min(st.session_state.timed_test_total_q, len(pool_q))
            st.session_state.timed_test_questions = pool_q[:tot_q]
            st.session_state.timed_test_total_q = tot_q
            st.session_state.timed_test_q_num = 1
            st.session_state.timed_test_score = 0
            st.session_state.timed_test_answers = []
            st.session_state.timed_test_missed = []
            st.session_state.timed_test_q_start_time = time.time()
            first_q = st.session_state.timed_test_questions[0]
            st.session_state.current_quiz_data = first_q

            return {
                "role": "assistant",
                "content": (
                    f"<div style='font-size: 1.1rem; font-weight: 700; color: #10b981; margin-bottom: 6px;'>🔄 Retaking Test ({tot_q} Questions)</div>\n\n"
                    f"• <b>Time Limit:</b> {st.session_state.timed_test_per_q_limit}s per question<br>"
                    f"• <i>Questions will appear below.</i>"
                )
            }

        # 2. Retake Missed Questions
        elif any(w in p for w in ["missed", "retry missed", "retake missed"]):
            if st.session_state.timed_test_missed:
                st.session_state.timed_test_active = True
                st.session_state.timed_test_questions = list(st.session_state.timed_test_missed)
                tot_missed = len(st.session_state.timed_test_questions)
                st.session_state.timed_test_total_q = tot_missed
                st.session_state.timed_test_q_num = 1
                st.session_state.timed_test_score = 0
                st.session_state.timed_test_answers = []
                st.session_state.timed_test_missed = []
                st.session_state.timed_test_q_start_time = time.time()
                first_q = st.session_state.timed_test_questions[0]
                st.session_state.current_quiz_data = first_q

                return {
                    "role": "assistant",
                    "content": (
                        f"<div style='font-size: 1.05rem; font-weight: 700; color: #f59e0b; margin-bottom: 6px;'>🔁 Retaking Missed Questions ({tot_missed} Questions)</div>\n\n"
                        f"• <b>Time Limit:</b> {st.session_state.timed_test_per_q_limit}s per question<br>"
                        f"• <i>Questions will appear below.</i>"
                    )
                }
            else:
                return {
                    "role": "assistant",
                    "content": "No missed questions left to retry!"
                }

        # 3. Quit Test
        else:
            st.session_state.timed_test_active = False
            st.session_state.current_quiz_data = None
            st.session_state.timed_test_missed = []
            return {
                "role": "assistant",
                "content": "Test finished. Good job!"
            }

    # Answering Ongoing Timed Test
    if st.session_state.timed_test_active:
        elapsed = round(time.time() - st.session_state.timed_test_q_start_time, 1)
        per_q_limit = st.session_state.timed_test_per_q_limit
        total_q = st.session_state.timed_test_total_q
        quiz_data = st.session_state.current_quiz_data or {}
        exp_corr = quiz_data.get("correct", "A")
        explanation = quiz_data.get("explanation", "")
        
        is_corr, explanation = viva.grade_viva(user_prompt, exp_corr, explanation)
        is_timeout = (elapsed > per_q_limit + 1.2)
        if is_timeout:
            is_corr = False
            
        if is_corr:
            st.session_state.timed_test_score += 1
        else:
            st.session_state.timed_test_missed.append(quiz_data)
            
        if "timed_test_answers" not in st.session_state:
            st.session_state.timed_test_answers = []
            
        st.session_state.timed_test_answers.append({
            "q_num": st.session_state.timed_test_q_num,
            "question": quiz_data.get("question", ""),
            "user_ans": user_prompt,
            "correct": exp_corr,
            "explanation": explanation,
            "is_corr": is_corr,
            "is_timeout": is_timeout,
            "elapsed": elapsed
        })

        # Check if all questions in test completed
        if st.session_state.timed_test_q_num >= total_q:
            st.session_state.timed_test_active = False
            st.session_state.current_quiz_data = None
            score = st.session_state.timed_test_score
            missed_cnt = len(st.session_state.timed_test_missed)
            pct = int((score / total_q) * 100) if total_q > 0 else 0
            
            # Format comprehensive end-of-test question review cards!
            review_cards = []
            for item in st.session_state.timed_test_answers:
                q_idx = item["q_num"]
                q_t = item["question"]
                u_a = item["user_ans"]
                c_k = item["correct"]
                exp = item["explanation"]
                el = item["elapsed"]
                
                if item["is_timeout"]:
                    badge = "<span style='color: #ef4444; font-weight: 700;'>⏰ TIME EXPIRED</span>"
                    status_line = f"{badge} (Took {el}s > {per_q_limit}s limit)"
                elif item["is_corr"]:
                    badge = "<span style='color: #10b981; font-weight: 700;'>✔ CORRECT</span>"
                    status_line = f"{badge} (Answered in {el}s)"
                else:
                    badge = "<span style='color: #f87171; font-weight: 700;'>✕ INCORRECT</span>"
                    status_line = f"{badge} (Answered in {el}s)"
                    
                rc = (
                    f"<div style='background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 12px 14px; margin-bottom: 10px;'>"
                    f"  <div style='font-size: 0.92rem; font-weight: 700; color: #e6edf3; margin-bottom: 4px;'>Question {q_idx}: {q_t}</div>"
                    f"  <div style='font-size: 0.86rem; color: #8b949e; margin-bottom: 6px;'>• <b>Result:</b> {status_line} | <b>Your Answer:</b> {u_a} | <b>Correct Option:</b> ({c_k})</div>"
                    f"  <div style='background: #0d1117; border-left: 3px solid #58a6ff; padding: 6px 10px; font-size: 0.84rem; color: #c9d1d9;'>💡 <b>Explanation:</b> {exp}</div>"
                    f"</div>"
                )
                review_cards.append(rc)
                
            review_html = "".join(review_cards)
            
            scorecard = (
                f"<div style='background: #161b22; border: 1px solid #10b981; border-radius: 8px; padding: 16px 20px; margin: 14px 0;'>"
                f"  <div style='font-size: 1.15rem; font-weight: 800; color: #10b981; margin-bottom: 8px;'>📊 Test Results</div>"
                f"  <div style='color: #e6edf3; font-size: 1rem; margin-bottom: 4px;'>• <b>Final Score:</b> <span style='color: #10b981; font-weight: 700;'>{score} / {total_q}</span> ({pct}%)</div>"
                f"  <div style='color: #8b949e; font-size: 0.88rem; margin-bottom: 4px;'>• <b>Time Limit:</b> {per_q_limit} seconds per question</div>"
                f"  <div style='color: #8b949e; font-size: 0.88rem;'>• Questions sourced from your uploaded files and Error Notebook.</div>"
                f"</div>"
            )
            
            st.session_state.asking_test_retry = True
            if missed_cnt > 0:
                action_text = f"<b style='color: #10b981;'>Test finished. Choose an option below: Retake whole test, retake missed questions ({missed_cnt}), or quit.</b>"
            else:
                action_text = (
                    f"<div style='color: #10b981; font-weight: 700; margin-bottom: 6px;'>🎉 Perfect Score! You got all questions right!</div>\n"
                    f"<b style='color: #10b981;'>Choose an option below: Retake whole test or quit.</b>"
                )

            return {
                "role": "assistant",
                "content": (
                    f"{scorecard}\n\n"
                    f"<div style='font-size: 0.95rem; font-weight: 700; color: #58a6ff; margin: 12px 0 8px 0;'>Question Review:</div>\n"
                    f"{review_html}\n\n"
                    f"{action_text}"
                )
            }
        else:
            # Advance to next test question WITHOUT revealing correctness or intermediate chat clutter!
            st.session_state.timed_test_q_num += 1
            next_q = st.session_state.timed_test_questions[st.session_state.timed_test_q_num - 1]
            st.session_state.current_quiz_data = next_q
            st.session_state.timed_test_q_start_time = time.time() # Reset timer for next question

            return None

    # Answering Error Notebook Quiz
    if st.session_state.error_quiz_active:
        st.session_state.error_quiz_active = False
        quiz_data = st.session_state.current_quiz_data or {}
        exp_corr = quiz_data.get("correct", "A")
        explanation = quiz_data.get("explanation", "")
        st.session_state.current_quiz_data = None
        
        is_corr, explanation = viva.grade_viva(user_prompt, exp_corr, explanation)
        
        expl_card = (
            f"<div style='background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; margin: 10px 0;'>"
            f"  <div style='font-size: 0.88rem; font-weight: 700; color: #58a6ff; margin-bottom: 4px;'>💡 Explanation:</div>"
            f"  <div style='color: #e6edf3; font-size: 0.9rem; line-height: 1.5;'>{explanation}</div>"
            f"</div>"
        )
        
        if is_corr:
            st.session_state.asking_quiz_permission = True
            return {
                "role": "assistant",
                "content": (
                    f"<div style='font-size: 1.05rem; font-weight: 700; color: #10b981; margin-bottom: 6px;'>"
                    f"✔ Correct! Option {exp_corr} is right.</div>\n\n"
                    f"{expl_card}\n\n"
                    f"<b>Would you like to try another quiz?</b>"
                )
            }
        else:
            return {
                "role": "assistant",
                "content": (
                    f"<div style='font-size: 1.05rem; font-weight: 700; color: #f59e0b; margin-bottom: 6px;'>"
                    f"• Incorrect — Option {exp_corr} was the right answer.</div>\n\n"
                    f"{expl_card}\n\n"
                    f"Tip: Check inputs at the start of your function to prevent crashes."
                )
            }

    # Answering ongoing Logic Quiz
    if st.session_state.quiz_active:
        quiz_data = st.session_state.current_quiz_data or {}
        exp_corr = quiz_data.get("correct", "A")
        explanation = quiz_data.get("explanation", "")
        
        is_corr, explanation = viva.grade_viva(user_prompt, exp_corr, explanation)
        
        if not is_corr:
            st.session_state.quiz_missed_questions.append(quiz_data)

        expl_card = (
            f"<div style='background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; margin: 10px 0;'>"
            f"  <div style='font-size: 0.88rem; font-weight: 700; color: #58a6ff; margin-bottom: 4px;'>💡 Explanation:</div>"
            f"  <div style='color: #e6edf3; font-size: 0.9rem; line-height: 1.5;'>{explanation}</div>"
            f"</div>"
        )
        
        status_hdr = (
            f"<div style='font-size: 1.05rem; font-weight: 700; color: #10b981; margin-bottom: 6px;'>✔ Correct! Option {exp_corr} is right.</div>"
            if is_corr else
            f"<div style='font-size: 1.05rem; font-weight: 700; color: #f59e0b; margin-bottom: 6px;'>• Incorrect — Option {exp_corr} was the right answer.</div>"
        )
        
        # Max 3 questions per session - CHECK FOR MISSED QUESTIONS ONLY AFTER LAST QUESTION!
        if st.session_state.quiz_question_num >= 3:
            st.session_state.quiz_active = False
            st.session_state.current_quiz_data = None
            st.session_state.quiz_question_num = 1
            missed_count = len(st.session_state.quiz_missed_questions)
            
            if missed_count > 0:
                st.session_state.asking_quiz_retry = True
                return {
                    "role": "assistant",
                    "content": (
                        f"{status_hdr}\n\n"
                        f"{expl_card}\n\n"
                        f"<div style='margin-top: 14px; padding: 12px 16px; background: #161b22; border: 1px solid #30363d; border-radius: 8px;'>"
                        f"  <div style='font-size: 1.05rem; font-weight: 700; color: #10b981;'>✔ Quiz Finished!</div>"
                        f"  <div style='color: #8b949e; margin-top: 4px;'>You got <b>{3 - missed_count} / 3 correct</b> ({missed_count} missed).</div>"
                        f"  <div style='color: #e6edf3; margin-top: 8px; font-weight: 600;'>Would you like to retry the questions you missed?</div>"
                        f"</div>"
                    )
                }
            else:
                return {
                    "role": "assistant",
                    "content": (
                        f"{status_hdr}\n\n"
                        f"{expl_card}\n\n"
                        f"<div style='margin-top: 14px; color: #10b981; font-weight: 700;'>🎉 Perfect Score: 3 / 3 (100%)! All answers were correct.</div>"
                    )
                }
        else:
            # Advance to next question - ONLY QUESTION, NO EXTRAS!
            st.session_state.quiz_question_num += 1
            next_data = viva.get_mutant_quiz_data(active_code, st.session_state.quiz_question_num)
            st.session_state.current_quiz_data = next_data

            return {
                "role": "assistant",
                "content": (
                    f"{status_hdr}\n\n"
                    f"{expl_card}\n\n"
                    f"<div style='margin-top: 12px;'><b>Question {st.session_state.quiz_question_num} of 3:</b> {next_data['question']}</div>"
                )
            }

    # User answering prompt: "Do you want to test your logic?"
    if st.session_state.asking_quiz_permission:
        st.session_state.asking_quiz_permission = False
        if any(w in p for w in ["yes", "sure", "ok", "yeah", "yep", "start", "quiz"]):
            st.session_state.quiz_active = True
            st.session_state.quiz_question_num = 1
            st.session_state.quiz_missed_questions = []
            q_data = viva.get_mutant_quiz_data(active_code, 1)
            st.session_state.current_quiz_data = q_data
            return {
                "role": "assistant",
                "content": f"<b>Question 1 of 3:</b> {q_data['question']}"
            }
        else:
            return {
                "role": "assistant",
                "content": "Understood. You can start the quiz anytime by clicking **Logic Quiz** above."
            }

    # User answering prompt: "Do you want to be questioned from this error note?"
    if st.session_state.asking_error_quiz_permission:
        st.session_state.asking_error_quiz_permission = False
        if any(w in p for w in ["clear", "delete", "empty"]):
            st.session_state.error_notebook = []
            return {
                "role": "assistant",
                "content": "<div style='color: #10b981; font-weight: 600;'>✔ All recorded failures have been cleared from your Error Notebook!</div>"
            }
        if any(w in p for w in ["yes", "sure", "ok", "yeah", "yep", "practice", "quiz"]):
            if st.session_state.error_notebook:
                st.session_state.error_quiz_active = True
                last_err = st.session_state.error_notebook[-1]
                q_data = viva.get_error_quiz_data(last_err)
                st.session_state.current_quiz_data = q_data
                return {
                    "role": "assistant",
                    "content": f"<b>Targeted Error Question ({last_err['func']}):</b> {q_data['question']}"
                }
            else:
                return {
                    "role": "assistant",
                    "content": "Your <b>Error Notebook</b> is empty! Run a test first to identify any edge cases."
                }
        else:
            return {
                "role": "assistant",
                "content": "Understood. You can review your Error Notebook, test code, or run quizzes anytime."
            }

    # 1. Timed Test Request (Open Setup Deck)
    if any(k in p for k in ["timed test", "start timed test", "create a test", "create test", "exam", "test me", "take test"]):
        st.session_state.show_test_setup = True
        return {
            "role": "assistant",
            "content": (
                "<div style='font-size: 1.05rem; font-weight: 700; color: #10b981; margin-bottom: 6px;'>⏱️ TIMED TEST SETUP</div>\n\n"
                "Please configure your test parameters above (select the number of questions and time limit from 5s to 30s) to begin."
            )
        }

    # 2. Clear Error Notebook request
    elif any(k in p for k in ["clear errors", "clear error", "clear notebook", "empty notebook"]):
        st.session_state.error_notebook = []
        save_error_notebook_to_disk([])
        st.session_state.asking_error_quiz_permission = False
        return {
            "role": "assistant",
            "content": "<div style='color: #10b981; font-weight: 600;'>✔ All recorded failures have been cleared from your Error Notebook!</div>"
        }

    # 2B. Delete specific error by number, e.g. "delete 1", "delete error 2", "remove 1"
    elif any(p.startswith(w) for w in ["delete", "remove", "del"]):
        import re
        del_match = re.search(r'\b(?:delete|remove|del)\s*(?:error\s*)?#?(\d+)\b', p)
        if del_match:
            target_idx = int(del_match.group(1)) - 1
            if 0 <= target_idx < len(st.session_state.error_notebook):
                removed = st.session_state.error_notebook.pop(target_idx)
                save_error_notebook_to_disk(st.session_state.error_notebook)
                return {
                    "role": "assistant",
                    "content": f"<div style='color: #10b981; font-weight: 600;'>✔ Deleted Error #{target_idx + 1} (<code>{removed['func']}</code>: {removed['type']}) from your Error Notebook!</div>\n\n" + format_error_notebook_bulletin()
                }
            else:
                return {
                    "role": "assistant",
                    "content": f"<div style='color: #f59e0b;'>⚠️ Error index #{target_idx + 1} was not found. Your notebook currently has {len(st.session_state.error_notebook)} entries.</div>"
                }

    # 3. Error Notebook request
    elif any(k in p for k in ["error notebook", "error note", "show error", "show errors", "my error", "my errors", "notebook", "bulletin", "error", "errors"]):
        notebook_text = format_error_notebook_bulletin()
        has_errors = bool(st.session_state.error_notebook)
        st.session_state.asking_error_quiz_permission = has_errors
        practice_prompt = "\n\n<b style='color: #10b981;'>You can delete any error entry below using the 🗑️ buttons, practice with an interactive question, or clear all.</b>" if has_errors else ""
        return {
            "role": "assistant",
            "content": f"{notebook_text}{practice_prompt}"
        }

    # 3. Test Code request
    elif any(k in p for k in ["test", "check", "run"]):
        inputs, mode = tester.get_test_inputs(active_code)
        success, output, exec_time = tester.run_code_sandbox(active_code, inputs)
        func_info = tester.inspect_function_details(active_code)
        func_name = func_info.get("func_name")

        if success:
            st.session_state.asking_quiz_permission = True
            st.session_state.last_error = ""  # Clear any past error since this run succeeded
            fn_title = f"function <code>{func_name}</code>" if func_name else "Python script"
            return {
                "role": "assistant",
                "content": (
                    f"<div style='font-size: 1.1rem; font-weight: 700; color: #10b981; margin-bottom: 8px;'>✔ All Tests Passed!</div>\n\n"
                    f"Your {fn_title} executed cleanly in <b>{exec_time}s</b> without crashing.\n\n"
                    f"<b>Would you like to try a quick logic quiz?</b>"
                )
            }
        else:
            st.session_state.last_error = output
            f_label = func_name or "script"
            record_error_in_notebook(f_label, output, inputs)

            hint = "<code style='color: #10b981; font-weight: 700;'>None</code>" if "NoneType" in output else "<code style='color: #10b981; font-weight: 700;'>edge input</code>"
            return {
                "role": "assistant",
                "content": (
                    f"<div style='font-size: 1rem; font-weight: 700; color: #f59e0b; margin-bottom: 6px;'>⚠ Test Failed:</div>\n\n"
                    f"The function crashed when tested with {hint}. "
                    f"This error has been saved to your <span style='color: #10b981; font-weight: 700;'>Error Notebook</span>.\n\n"
                    f"Click <b style='color: #10b981;'>Fix Code</b> above to automatically fix this issue."
                )
            }

    # 4. Fix Code request WITH STRUCTURED ERROR ANALYSIS!
    elif any(k in p for k in ["fix", "heal", "safety", "protect", "patch", "error analysis", "analysis"]):
        func_info = tester.inspect_function_details(active_code)
        
        # Only run sandbox test if last_error is empty AND there is an actual function to test
        if not st.session_state.last_error and func_info.get("func_name"):
            inputs, _ = tester.get_test_inputs(active_code)
            ok, output, _ = tester.run_code_sandbox(active_code, inputs)
            if not ok:
                st.session_state.last_error = output
            else:
                st.session_state.last_error = ""

        healed, note, diff_str, analysis = healer.repair_code(active_code, st.session_state.last_error)
        st.session_state.healed_code = healed
        st.session_state.current_code = healed

        saved_file_note = ""
        # Only overwrite the file on disk if changes were actually made!
        if healed != active_code:
            active_path = st.session_state.get("active_file_path")
            if active_path and os.path.exists(os.path.dirname(active_path)):
                try:
                    with open(active_path, "w", encoding="utf-8") as f:
                        f.write(healed)
                    fname = os.path.basename(active_path)
                    saved_file_note = (
                        f"<div style='margin-top: 10px; color: #10b981; font-weight: 600; font-size: 0.9rem;'>"
                        f"✔ Saved: <code>{fname}</code> was updated with the fixed code.</div>"
                    )
                except Exception:
                    pass
        else:
            saved_file_note = (
                f"<div style='margin-top: 10px; color: #10b981; font-weight: 600; font-size: 0.9rem;'>"
                f"✔ Code is already clean. No modifications needed.</div>"
            )

        is_no_change = (healed == active_code)
        card_title = "🔍 Code Verification:" if is_no_change else "🔍 Error Details:"
        hdr_color = "#10b981" if is_no_change else "#f59e0b"
        status_color = "#10b981" if is_no_change else "#f87171"

        error_analysis_card = (
            f"<div style='background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 14px 18px; margin: 12px 0;'>"
            f"  <div style='font-size: 0.95rem; font-weight: 700; color: {hdr_color}; margin-bottom: 8px;'>{card_title}</div>"
            f"  <div style='color: #e6edf3; font-size: 0.88rem; margin-bottom: 5px;'>• <b>Target:</b> <code style='color: #58a6ff;'>{analysis['function']}</code></div>"
            f"  <div style='color: #e6edf3; font-size: 0.88rem; margin-bottom: 5px;'>• <b>Status:</b> <span style='color: {status_color}; font-weight: 600;'>{analysis['vulnerability']}</span></div>"
            f"  <div style='color: #8b949e; font-size: 0.88rem; margin-bottom: 5px;'>• <b>Details:</b> {analysis['root_cause']}</div>"
            f"  <div style='color: #10b981; font-size: 0.88rem;'>• <b>Action:</b> {analysis['remediation']}</div>"
            f"</div>"
        )

        if is_no_change:
            return {
                "role": "assistant",
                "content": (
                    f"<div style='font-size: 1.1rem; font-weight: 700; color: #10b981; margin-bottom: 6px;'>✔ Code Verified: Already Clean</div>\n\n"
                    f"{error_analysis_card}\n"
                    f"{saved_file_note}"
                ),
                "healed_code": healed
            }
        else:
            return {
                "role": "assistant",
                "content": (
                    f"<div style='font-size: 1.1rem; font-weight: 700; color: #10b981; margin-bottom: 6px;'>✔ Code Fixed: {note}</div>\n\n"
                    f"{error_analysis_card}\n"
                    f"Here is your updated code:\n"
                    f"{saved_file_note}"
                ),
                "healed_code": healed
            }

    # 5. Logic Quiz request - ONLY QUESTION, NO EXTRAS!
    elif any(k in p for k in ["quiz", "viva", "test logic", "question"]):
        st.session_state.quiz_active = True
        st.session_state.quiz_question_num = 1
        st.session_state.quiz_missed_questions = []
        q_data = viva.get_mutant_quiz_data(active_code, 1)
        st.session_state.current_quiz_data = q_data
        return {
            "role": "assistant",
            "content": f"<b>Question 1 of 3:</b> {q_data['question']}"
        }

    # 6. General conversation
    else:
        return {
            "role": "assistant",
            "content": (
                f"Instruction: \"{user_prompt}\"\n\n"
                "You can execute <b>Test Code</b>, <b>Fix Code</b>, <b>Logic Quiz</b>, <b>Timed Test</b>, or review your <b>Error Notebook</b> above."
            )
        }

# -------------------------------------------------------------
# 10. CHAT STREAM
# -------------------------------------------------------------
for msg in st.session_state.messages:
    role = msg["role"]
    avatar_img = BOT_AVATAR_PATH if role == "assistant" else USER_AVATAR_PATH
    with st.chat_message(role, avatar=avatar_img):
        st.markdown(msg["content"], unsafe_allow_html=True)
        
        if "healed_code" in msg:
            st.code(msg["healed_code"], language="python")

# Anchor at the end of the chat stream for auto-scrolling
st.markdown('<div id="latest-response-anchor"></div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 11. INTERACTIVE QUESTIONING / OPTIONS STACK (CLEAN, NO EXTRAS)
# -------------------------------------------------------------
interactive_answer = None

# Case A: Active Question in Logic Quiz, Error Quiz, or Timed Test -> CLEAN STACK
if (st.session_state.quiz_active or st.session_state.error_quiz_active or st.session_state.timed_test_active) and st.session_state.current_quiz_data:
    q_data = st.session_state.current_quiz_data
    options = q_data.get("options", [])
    
    if st.session_state.timed_test_active:
        per_q_limit = st.session_state.timed_test_per_q_limit
        total_q = st.session_state.timed_test_total_q
        header_title = f"⏱️ Timed Test — Question {st.session_state.timed_test_q_num} of {total_q}"
        
        # Real-time ticking digital counter
        st.html(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 0.92rem; color: #f59e0b; padding: 4px 10px; background: #161b22; border-radius: 6px; border: 1px solid #30363d; margin-bottom: 2px;">
            <span style="font-weight: 700;">⏱️ Question Timer ({per_q_limit}s Limit)</span>
            <span id="ticker" style="background: #0d1117; border: 1px solid #30363d; border-radius: 4px; padding: 2px 10px; font-weight: 800; font-family: monospace; font-size: 0.95rem; color: #f59e0b;">
                ⏳ <span id="s_left">{per_q_limit}</span>s remaining
            </span>
        </div>
        <script>
            var left = {per_q_limit};
            var t_elem = document.getElementById('s_left');
            var box = document.getElementById('ticker');
            var iv = setInterval(function() {{
                left--;
                if (left >= 0) {{
                    t_elem.textContent = left;
                    if (left <= 5) {{
                        box.style.color = '#ef4444';
                        box.style.borderColor = '#ef4444';
                    }}
                }} else {{
                    clearInterval(iv);
                    box.innerHTML = '<span style="color: #ef4444; font-weight: 800;">⏰ TIME EXPIRED</span>';
                }}
            }}, 1000);
        </script>
        """, unsafe_allow_javascript=True)

        # Smooth CSS Keyframe progress bar that shrinks from 100% to 0% over {per_q_limit}s
        st.html(f"""
        <div style="margin: 4px 0 10px 0;">
            <div style="background: #21262d; border-radius: 4px; height: 6px; width: 100%; overflow: hidden; border: 1px solid #30363d;">
                <div style="height: 100%; animation: q_timer_bar_{st.session_state.timed_test_q_num} {per_q_limit}s linear forwards;"></div>
            </div>
        </div>
        <style>
        @keyframes q_timer_bar_{st.session_state.timed_test_q_num} {{
            0% {{ width: 100%; background-color: #10b981; }}
            50% {{ width: 50%; background-color: #f59e0b; }}
            80% {{ width: 20%; background-color: #ef4444; }}
            100% {{ width: 0%; background-color: #ef4444; }}
        }}
        </style>
        """)
    else:
        header_title = f"Question {st.session_state.quiz_question_num} of 3"

    st.markdown(f"""
    <div class="interactive-quiz-box">
        <div class="interactive-quiz-header">{header_title}</div>
        <div class="interactive-quiz-question">{q_data.get('question', '')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Vertically stacked full-width option cards - ONLY OPTIONS, NO EXTRAS!
    for opt in options:
        btn_label = f"({opt['key']})   {opt['text']}"
        if st.button(btn_label, key=f"quiz_opt_{opt['key']}", use_container_width=True):
            interactive_answer = f"Option {opt['key']}: {opt['text']}"
            
    stop_label = "⏹ Stop Test" if st.session_state.timed_test_active else "⏹ Stop Quiz"
    if st.button(stop_label, key="btn_stop_quiz", use_container_width=True):
        interactive_answer = "stop"

# Case B: Re-attempting missed quiz questions prompt (Only after question 3!)
elif st.session_state.asking_quiz_retry:
    st.markdown("""
    <div style="background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; margin: 10px 0;">
        <span style="color: #10b981; font-weight: 600; font-size: 0.95rem;">Would you like to retry the questions you missed?</span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔁 Yes, Retry Missed Questions", key="btn_quiz_retry_yes", use_container_width=True):
        interactive_answer = "retry missed questions"
    if st.button("✕ No, Conclude Quiz", key="btn_quiz_retry_no", use_container_width=True):
        interactive_answer = "finish"

# Case C: Post-Test Options -> Retake whole test, retake missed questions, quit test
elif st.session_state.asking_test_retry:
    st.markdown("""
    <div style="background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; margin: 10px 0;">
        <span style="color: #10b981; font-weight: 600; font-size: 0.95rem;">Test completed! Choose your next action:</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Retake Whole Test", key="btn_test_retake_whole", use_container_width=True):
        interactive_answer = "retake whole test"

    missed_count = len(st.session_state.timed_test_missed)
    if missed_count > 0:
        if st.button(f"🔁 Retake Missed Questions ({missed_count})", key="btn_test_retake_missed", use_container_width=True):
            interactive_answer = "retake missed questions"

    if st.button("⏹ Quit Test", key="btn_test_quit", use_container_width=True):
        interactive_answer = "quit test"

# Case D: Permission prompt for Logic Quiz -> VERTICAL STACK
elif st.session_state.asking_quiz_permission:
    st.markdown("""
    <div style="background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; margin: 10px 0;">
        <span style="color: #10b981; font-weight: 600; font-size: 0.95rem;">Ready to test your logic with interactive questions?</span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("✔ Yes, Start Logic Quiz", key="btn_start_quiz_yes", use_container_width=True):
        interactive_answer = "yes"
    if st.button("✕ No, Maybe Later", key="btn_start_quiz_no", use_container_width=True):
        interactive_answer = "no"

# Case E: Permission prompt for Error Notebook Quiz -> CLEAN STACK WITH INDIVIDUAL DELETES
elif st.session_state.asking_error_quiz_permission:
    if st.session_state.error_notebook:
        st.markdown("""
        <div style="background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 10px 14px; margin: 10px 0 8px 0;">
            <span style="color: #10b981; font-weight: 700; font-size: 0.95rem;">🗑️ Delete Error Entries:</span>
        </div>
        """, unsafe_allow_html=True)

        for idx, item in enumerate(st.session_state.error_notebook):
            col_err_txt, col_err_del = st.columns([5, 1])
            with col_err_txt:
                st.markdown(
                    f"<div style='padding: 6px 0; border-bottom: 1px solid #21262d;'>"
                    f"<b>[{idx+1}] Function:</b> <code style='color: #58a6ff;'>{item['func']}</code> | "
                    f"<b>Error:</b> <span style='color: #f59e0b; font-weight: 600;'>{item['type']}</span><br>"
                    f"<span style='color: #8b949e; font-size: 0.85rem; margin-left: 8px;'><i>Cause:</i> {item['reason']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            with col_err_del:
                if st.button("🗑️ Delete", key=f"del_err_btn_{idx}_{item.get('func', '')}", use_container_width=True):
                    removed = st.session_state.error_notebook.pop(idx)
                    save_error_notebook_to_disk(st.session_state.error_notebook)
                    st.toast(f"✔ Removed error for '{removed.get('func', 'function')}'!")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"<div style='color: #10b981; font-weight: 600;'>✔ Removed failure record for <code>{removed.get('func', 'function')}</code> ({removed.get('type', 'Error')}) from your Error Notebook.</div>"
                    })
                    if not st.session_state.error_notebook:
                        st.session_state.asking_error_quiz_permission = False
                    st.rerun()

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        col_ep1, col_ep2, col_ep3 = st.columns([2, 1, 1])
        with col_ep1:
            if st.button("🎯 Practice This Error", key="btn_error_quiz_yes", use_container_width=True):
                interactive_answer = "yes"
        with col_ep2:
            if st.button("🗑️ Clear All", key="btn_error_quiz_clear", use_container_width=True):
                interactive_answer = "clear"
        with col_ep3:
            if st.button("✕ Close", key="btn_error_quiz_no", use_container_width=True):
                interactive_answer = "no"

# -------------------------------------------------------------
# 12. AUTO-SCROLL TO LATEST RESPONSE (DISABLED FOR TIMED TEST ALONE)
# -------------------------------------------------------------
if not st.session_state.timed_test_active:
    st.html("""
    <script>
        function scrollToLatest() {
            try {
                const doc = window.parent.document;
                const anchor = doc.getElementById("latest-response-anchor");
                if (anchor) {
                    anchor.scrollIntoView({ behavior: "smooth", block: "end" });
                } else {
                    const main = doc.querySelector("section.main") || doc.documentElement;
                    if (main) main.scrollTo({ top: main.scrollHeight, behavior: "smooth" });
                }
            } catch (e) {
                console.error("Scroll error:", e);
            }
        }
        setTimeout(scrollToLatest, 60);
    </script>
    """, unsafe_allow_javascript=True)

# -------------------------------------------------------------
# 13. CHAT INPUT & EXECUTION
# -------------------------------------------------------------
user_text = st.chat_input("Type your answer, or type 'quiz', 'test', 'errors'...")
action_to_run = interactive_answer or btn_trigger or user_text

if action_to_run:
    was_timed_active = st.session_state.timed_test_active
    response = process_user_input(action_to_run)

    # For timed test intermediate questions, keep viewport steady on the front card
    if not (was_timed_active and st.session_state.timed_test_active):
        st.session_state.messages.append({"role": "user", "content": action_to_run})
        if response:
            st.session_state.messages.append(response)

    st.rerun()
