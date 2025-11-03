import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Student Grading System", layout="centered")

# --- Helpers ---
def compute_grade(avg):
    """Return letter grade for given average (0-100). Uses if/elif/else."""
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

def students_to_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode('utf-8')

# Initialize session state to store students across interactions
if "students" not in st.session_state:
    st.session_state.students = []  # list of dicts: {"Name", "Marks", "Average", "Grade"}

st.title("🎓 Student Grading System — Streamlit")
st.markdown(
    "Enter student names and three subject marks. The app will validate entries, compute the average, assign a grade, display a table, "
    "and let you download the results as CSV."
)

# --- Input form ---
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
    # Validation
    errors = []
    if not validate_name(name):
        errors.append("Name cannot be empty.")
    if not validate_score(m1):
        errors.append("Subject 1 must be a number between 0 and 100.")
    if not validate_score(m2):
        errors.append("Subject 2 must be a number between 0 and 100.")
    if not validate_score(m3):
        errors.append("Subject 3 must be a number between 0 and 100.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        scores = [float(m1), float(m2), float(m3)]
        avg = sum(scores) / len(scores)
        grade = compute_grade(avg)

        student_record = {
            "Name": name.strip(),
            "Subject 1": scores[0],
            "Subject 2": scores[1],
            "Subject 3": scores[2],
            "Average": round(avg, 2),
            "Grade": grade,
        }

        st.session_state.students.append(student_record)
        st.success(f"Added {name.strip()} — Avg: {avg:.2f} — Grade: {grade}")

# --- Display table and controls ---
st.subheader("Class Results")
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)

    # Show table
    st.dataframe(df, use_container_width=True)

    # Simple statistics using for loop to compute grade distribution
    grade_counts = {}
    for g in df["Grade"]:
        grade_counts[g] = grade_counts.get(g, 0) + 1

    st.markdown("**Grade distribution:**")
    st.write(grade_counts)

    # CSV download
    csv_bytes = students_to_csv(df)
    st.download_button(
        label="📥 Download results as CSV",
        data=csv_bytes,
        file_name="student_grades.csv",
        mime="text/csv",
    )

    # Option to clear all
    if st.button("🗑️ Clear all students"):
        st.session_state.students = []
        st.experimental_rerun()
else:
    st.info("No students added yet. Use the form above to add students.")

# --- Loops Playground: show simple examples of if, for, while ---
st.subheader("Loops Playground — see `if`, `for`, and `while` in action")

with st.expander("If statement example (pass/fail)"):
    st.write("This uses an if/elif/else to classify a single score.")
    score = st.slider("Pick a sample score", 0, 100, 73)
    if score >= 50:
        st.success(f"Score {score}: PASS")
    else:
        st.error(f"Score {score}: FAIL")

with st.expander("For loop example (process a list of names)"):
    st.write("We iterate over a list of names using a `for` loop and display greetings.")
    sample_names = st.text_area("Enter names separated by commas", "Alice,Bob,Charlie")
    if st.button("Run for-loop greetings", key="for_run"):
        names_list = [n.strip() for n in sample_names.split(",") if n.strip()]
        greetings = []
        for n in names_list:  # for loop here
            greetings.append(f"Hello, {n}!")
        st.write("\n".join(greetings))

with st.expander("While loop example (countdown)"):
    st.write("This demonstrates a `while` loop with a simple countdown.")
    start = st.number_input("Start countdown from", min_value=1, max_value=30, value=5, step=1)
    if st.button("Run countdown", key="while_run"):
        # We'll build the output rather than block the UI too long
        cnt = start
        out = []
        while cnt > 0:
            out.append(f"T-minus {cnt}")
            cnt -= 1
        out.append("Liftoff!")
        st.write("\n".join(out))

st.markdown("---")
st.caption("App built with Streamlit — enter students, validate data, compute grades and export results.")
