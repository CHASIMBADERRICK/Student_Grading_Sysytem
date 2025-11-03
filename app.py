import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Student Grading System", layout="centered")

# --- Helper functions ---
def compute_grade(avg):
    """Return letter grade for given average (0-100)."""
    if avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"

def validate_name(name: str) -> bool:
    return bool(name and name.strip())

def validate_score(score) -> bool:
    try:
        s = float(score)
        return 0 <= s <= 100
    except Exception:
        return False

# --- File setup (autosave path) ---
CSV_FILE = "student_grades.csv"

# Load existing data on startup  # NEW
if os.path.exists(CSV_FILE):
    existing_df = pd.read_csv(CSV_FILE)
    st.session_state.students = existing_df.to_dict(orient="records")
else:
    if "students" not in st.session_state:
        st.session_state.students = []

# --- Title & Instructions ---
st.title("🎓 Student Grading System — Streamlit (Auto-Save)")
st.markdown(
    "Enter student names and marks for three subjects. The app will automatically validate input, "
    "compute averages, assign grades, display the table, and **auto-save all records to CSV** (`student_grades.csv`)."
)

# --- Student entry form ---
with st.form("student_form", clear_on_submit=True):
    st.subheader("Add a student")
    name = st.text_input("Student name")
    col1, col2, col3 = st.columns(3)
    with col1:
        m1 = st.text_input("Subject 1 (0–100)")
    with col2:
        m2 = st.text_input("Subject 2 (0–100)")
    with col3:
        m3 = st.text_input("Subject 3 (0–100)")

    submitted = st.form_submit_button("Add student")

if submitted:
    errors = []
    if not validate_name(name):
        errors.append("Name cannot be empty.")
    if not validate_score(m1):
        errors.append("Subject 1 must be between 0 and 100.")
    if not validate_score(m2):
        errors.append("Subject 2 must be between 0 and 100.")
    if not validate_score(m3):
        errors.append("Subject 3 must be between 0 and 100.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        scores = [float(m1), float(m2), float(m3)]
        avg = sum(scores) / len(scores)
        grade = compute_grade(avg)
        student = {
            "Name": name.strip(),
            "Subject 1": scores[0],
            "Subject 2": scores[1],
            "Subject 3": scores[2],
            "Average": round(avg, 2),
            "Grade": grade,
        }
        st.session_state.students.append(student)

        # Auto-save to CSV  # NEW
        df = pd.DataFrame(st.session_state.students)
        df.to_csv(CSV_FILE, index=False)
        st.success(f"Added {name.strip()} — Avg: {avg:.2f}, Grade: {grade}. Data auto-saved ✅")

# --- Display results ---
st.subheader("📋 Class Results")
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)
    st.dataframe(df, use_container_width=True)

    # Grade distribution using for loop
    grade_counts = {}
    for g in df["Grade"]:
        grade_counts[g] = grade_counts.get(g, 0) + 1
    st.write("**Grade distribution:**", grade_counts)

    # CSV download
    st.download_button(
        label="📥 Download current CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="student_grades.csv",
        mime="text/csv",
    )

    # Clear all data (with confirmation)
    if st.button("🗑️ Clear all records"):
        st.session_state.students = []
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)  # delete file  # NEW
        st.success("All records cleared and CSV deleted.")
        st.experimental_rerun()
else:
    st.info("No students added yet. Use the form above to begin.")

# --- Loops Playground ---
st.subheader("🧠 Loops Playground (Educational)")

with st.expander("If statement example"):
    score = st.slider("Test score", 0, 100, 72)
    if score >= 50:
        st.success(f"Score {score}: PASS")
    else:
        st.error(f"Score {score}: FAIL")

with st.expander("For loop example"):
    names_text = st.text_area("Names (comma-separated)", "Alice,Bob,Charlie")
    if st.button("Run for-loop greetings"):
        names = [n.strip() for n in names_text.split(",") if n.strip()]
        greetings = []
        for n in names:
            greetings.append(f"Hello, {n}!")  # for loop in action
        st.write("\n".join(greetings))

with st.expander("While loop example"):
    start = st.number_input("Start countdown from", 1, 10, 5)
    if st.button("Run countdown"):
        cnt = start
        output = []
        while cnt > 0:
            output.append(f"T-minus {cnt}")
            cnt -= 1
        output.append("Liftoff!")
        st.write("\n".join(output))

st.markdown("---")
st.caption("This Streamlit app demonstrates if/for/while loops, grading logic, and CSV auto-saving.")
