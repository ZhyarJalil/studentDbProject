import sqlite3
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Student Database", layout="centered")
st.title("🎓 Student Record Management System")


# --- DATABASE FUNCTIONS ---
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            major TEXT NOT NULL,
            grade TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def add_student(name, major, grade):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, major, grade) VALUES (?, ?, ?)",
        (name, major, grade),
    )
    conn.commit()
    conn.close()


def get_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()
    return data


def delete_student(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()


# Initialize DB
init_db()

# --- UI LAYOUT ---

# Form to Add Student
st.subheader("Add New Student")
with st.form("student_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Name", placeholder="John Doe")
    with col2:
        major = st.text_input("Major", placeholder="Computer Science")
    with col3:
        grade = st.text_input("Grade", placeholder="A")

    submit = st.form_submit_with_button("Add Student")
    if submit:
        if name and major and grade:
            add_student(name, major, grade)
            st.success(f"Added {name} successfully!")
        else:
            st.error("All fields are required")

# Display and Delete Section
st.subheader("Current Records")
records = get_students()

if records:
    # Format data into a clean list for selection
    options = {f"ID {r[0]}: {r[1]} ({r[2]}) - Grade: {r[3]}": r[0] for r in records}

    # Show a dropdown to delete records
    to_delete = st.selectbox("Select a student to remove:", list(options.keys()))
    if st.button("Delete Selected Student", type="primary"):
        delete_student(options[to_delete])
        st.toast("Record deleted successfully!")
        st.rerun()

    st.markdown("---")
    # Display data table beautifully
    st.dataframe(
        records,
        column_config={
            0: "ID",
            1: "Student Name",
            2: "Major / Department",
            3: "Final Grade",
        },
        use_container_width=True,
    )
else:
    st.info("No records found in the database. Add a student above!")