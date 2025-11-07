import streamlit as st
import pandas as pd
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Student Grading System", layout="wide")

# Grading function helper

def compute_grade(avg):
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
    """Generate PDF report for a student."""
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


#  Simple Login System

TEACHERS = {
    "teacher1": "password123",
    "admin": "admin123"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Teacher Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in TEACHERS and TEACHERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username} 👩‍🏫")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")
    st.stop()


#  Main Grading System

st.title(f"🎓 Student Grading System — Logged in as {st.session_state.username}")

CSV_FILE = "student_grades.csv"

if os.path.exists(CSV_FILE):
    df_existing = pd.read_csv(CSV_FILE)
    st.session_state.students = df_existing.to_dict(orient="records")
else:
    if "students" not in st.session_state:
        st.session_state.students = []

# Sidebar
st.sidebar.header("⚙️ Configuration")
num_subjects = st.sidebar.slider("Number of subjects", 1, 10, 3)
subject_names = [f"Subject {i+1}" for i in range(num_subjects)]
CSV_COLUMNS = ["Name"] + subject_names + ["Average", "Grade"]

# --- Dashboard Summary ---
st.subheader("📊 Class Dashboard Summary")
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)
    class_avg = round(df["Average"].mean(), 2)
    top_student = df.loc[df["Average"].idxmax()]["Name"]
    top_score = df["Average"].max()
    bottom_student = df.loc[df["Average"].idxmin()]["Name"]
    bottom_score = df["Average"].min()
    pass_rate = (df[df["Average"] >= 50].shape[0] / len(df)) * 100

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🏫 Class Average", class_avg)
    col2.metric("🥇 Top Student", f"{top_student}", f"{top_score:.1f}")
    col3.metric("🥈 Lowest Student", f"{bottom_student}", f"{bottom_score:.1f}")
    col4.metric("📈 Pass Rate", f"{pass_rate:.1f}%")
    col5.metric("👩‍🎓 Total Students", len(df))
else:
    st.info("No student data yet. Add students below to see dashboard insights.")

# --- Add Student ---
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
                st.error(f"{subj} must be between 0 and 100.")
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

# --- Display Class Results ---
st.subheader("📋 Class Results")
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)
    st.dataframe(df, use_container_width=True)

    # Charts
    st.subheader("📊 Grade Distribution")
    st.bar_chart(df["Grade"].value_counts().sort_index())

    st.subheader("📈 Average Comparison per Student")
    st.line_chart(df[["Name", "Average"]].set_index("Name"))

    # PDF Reports
    st.subheader("📄 Generate Student PDF Report")
    student_names = df["Name"].tolist()
    selected_student = st.selectbox("Select a student", student_names)
    if st.button("Generate PDF"):
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

    # CSV Download & Clear All
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
        st.success("All records cleared.")
        st.experimental_rerun()
else:
    st.info("No student data available yet.")

# --- Loops Playground ---
st.subheader(" Loops Playground")
with st.expander("If Example"):
    score = st.slider("Test score", 0, 100, 72)
    if score >= 50:
        st.success(f"Score {score}: PASS")
    else:
        st.error(f"Score {score}: FAIL")

with st.expander("For Loop Example"):
    names_text = st.text_area("Names (comma-separated)", "Alice,Bob,Charlie")
    if st.button("Run For Loop"):
        names = [n.strip() for n in names_text.split(",") if n.strip()]
        greetings = [f"Hello, {n}!" for n in names]
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

# --- Logout Button ---
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.experimental_rerun()
