import streamlit as st
import pandas as pd
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

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

def validate_score(score) -> bool:
    try:
        s = float(score)
        return 0 <= s <= 100
    except Exception:
        return False

def make_pdf(student: dict):
    """Generate a simple PDF report for one student."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 800, f"Student Report: {student['Name']}")
    c.setFont("Helvetica", 12)

    y = 760
    for subject, mark in student["Subjects"].items():
        c.drawString(100, y, f"{subject}: {mark}")
        y -= 20

    c.drawString(100, y - 10, f"Average: {student['Average']}")
    c.drawString(100, y - 30, f"Grade: {student['Grade']}")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- File persistence ---
CSV_FILE = "student_grades.csv"

# Load data from CSV on startup
if os.path.exists(CSV_FILE):
    df_existing = pd.read_csv(CSV_FILE)
    st.session_state.students = df_existing.to_dict(orient="records")
else:
    if "students" not in st.session_state:
        st.session_state.students = []

# --- App Header ---
st.title("🎓 Streamlit Student Grading System")
st.markdown("""
This web app lets teachers dynamically select how many subjects to grade,  
auto-saves to CSV, visualizes results, and generates **PDF reports** for each student.
""")

# --- Dynamic Subject Setup ---
st.sidebar.header("⚙️ Configuration")
num_subjects = st.sidebar.slider("Number of subjects", 1, 10, 3)
subject_names = [f"Subject {i+1}" for i in range(num_subjects)]
CSV_COLUMNS = ["Name"] + subject_names + ["Average", "Grade"]

# --- Input Form ---
with st.form("student_form", clear_on_submit=True):
    st.subheader("➕ Add New Student")
    name = st.text_input("Student name")

    cols = st.columns(num_subjects)
    marks = {}
    for i, col in enumerate(cols):
        with col:
            marks[subject_names[i]] = st.text_input(f"{subject_names[i]} (0–100)")

    submitted = st.form_submit_button("Add Student")

if submitted:
    if not name.strip():
        st.error("Name cannot be empty.")
    else:
        valid = True
        scores = []
        for subj, val in marks.items():
            if not validate_score(val):
                st.error(f"{subj} must be a number between 0–100.")
                valid = False
            else:
                scores.append(float(val))

        if valid:
            avg = sum(scores) / len(scores)
            grade = compute_grade(avg)

            student_record = {
                "Name": name.strip(),
                **{subj: marks[subj] for subj in subject_names},
                "Average": round(avg, 2),
                "Grade": grade,
            }

            st.session_state.students.append(student_record)
            pd.DataFrame(st.session_state.students)[CSV_COLUMNS].to_csv(CSV_FILE, index=False)
            st.success(f"Added {name.strip()} — Avg: {avg:.2f}, Grade: {grade}. Auto-saved ✅")

# --- Display Results ---
st.subheader("📋 Class Results")
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)
    st.dataframe(df, use_container_width=True)

    # --- Charts ---
    st.subheader("📊 Grade Distribution")
    grade_counts = df["Grade"].value_counts().sort_index()
    st.bar_chart(grade_counts)

    st.subheader("📈 Average Comparison per Student")
    avg_chart = df[["Name", "Average"]].set_index("Name")
    st.line_chart(avg_chart)

    # --- PDF Download ---
    st.subheader("📄 Download Individual Student Reports")
    student_names = df["Name"].tolist()
    selected_student = st.selectbox("Choose a student", student_names)
    if st.button("Generate PDF Report"):
        student_row = df[df["Name"] == selected_student].iloc[0].to_dict()
        subjects_dict = {k: student_row[k] for k in subject_names}
        student_info = {
            "Name": selected_student,
            "Subjects": subjects_dict,
            "Average": student_row["Average"],
            "Grade": student_row["Grade"],
        }
        pdf = make_pdf(student_info)
        st.download_button(
            label=f"⬇️ Download {selected_student}'s Report",
            data=pdf,
            file_name=f"{selected_student}_report.pdf",
            mime="application/pdf",
        )

    # --- CSV Download & Clear ---
    st.download_button(
        label="📥 Download Full CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="student_grades.csv",
        mime="text/csv",
    )

    if st.button("🗑️ Clear All Records"):
        st.session_state.students = []
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
        st.success("All data cleared.")
        st.experimental_rerun()
else:
    st.info("No students yet. Add some using the form above.")

# --- Educational Section ---
st.subheader("Loops Playground")
with st.expander("If Statement Example"):
    score = st.slider("Test score", 0, 100, 72)
    if score >= 50:
        st.success(f"Score {score}: PASS")
    else:
        st.error(f"Score {score}: FAIL")

with st.expander("For Loop Example"):
    names_text = st.text_area("Enter names separated by commas", "Alice,Bob,Charlie")
    if st.button("Run Greetings"):
        names = [n.strip() for n in names_text.split(",") if n.strip()]
        greetings = []
        for n in names:
            greetings.append(f"Hello, {n}!")  # for loop in action
        st.write("\n".join(greetings))

with st.expander("While Loop Example"):
    start = st.number_input("Start countdown from", 1, 10, 5)
    if st.button("Run Countdown"):
        cnt = start
        output = []
        while cnt > 0:
            output.append(f"T-minus {cnt}")
            cnt -= 1
        output.append("Liftoff!")
        st.write("\n".join(output))

st.markdown("---")
st.caption("Built with  Streamlit — featuring dynamic subjects, auto-save, charts, and PDF reports.")
