import sqlite3
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Student Database", layout="centered")
st.title("Student Record Management System")


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
    
    # 1. Delete the student
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    
    # 2. Check if the table is now completely empty
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    
    # 3. If empty, completely reset the internal auto-increment counter back to 0
    if count == 0:
        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'students'")
        
    conn.commit()
    conn.close()


# Initialize DB
init_db()

# --- UI LAYOUT ---

# Form to Add Student (Visible to Everyone)
st.subheader("Add New Student")
with st.form("student_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Name", placeholder="Zhyar Jalil")
    with col2:
        major = st.text_input("Major", placeholder="Computer Engineer")
    with col3:
        grade = st.text_input("Grade", placeholder="Third")

    submit = st.form_submit_button("Add Student", help="Hi")
    if submit:
        if name and major and grade:
            add_student(name, major, grade)
            st.success(f"Added {name} successfully!")
        else:
            st.error("All fields are required")

# Display Section (Visible to Everyone)
# Display Section (Visible to Everyone)
st.subheader("Current Records")
records = get_students()

if records:
    import pandas as pd

    # 1. Load the data with headers
    df = pd.DataFrame(records, columns=["ID", "Student Name", "Major / Department", "Final Grade"])
    
    # 2. Drop the ID column visually (axis=1 means drop a column, not a row)
    df_visible = df.drop(columns=["ID"])
    
    # 3. Display the new table without the ID column
    st.dataframe(
        df_visible,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # --- ADMIN ONLY SECTION ---
    st.subheader("Admin Controls")

    # Password input field (masks the typing)
    admin_password = st.text_input(
        "Enter Admin Password to reveal Delete tools:", type="password"
    )

    # Check if the password matches
    if admin_password == "admin123":
        st.success("Access Granted!")

        # Format data into a clean list for selection
        options = {
            f"ID {r[0]}: {r[1]} ({r[2]}) - Grade: {r[3]}": r[0] for r in records
        }

        # Show the dropdown and delete button ONLY if password is correct
        to_delete = st.selectbox("Select a student to remove:", list(options.keys()))
        if st.button("Delete Selected Student", type="primary"):
            delete_student(options[to_delete])
            st.toast("Record deleted successfully!")
            st.rerun()
    elif admin_password != "":
        st.error("Incorrect Password")

else:
    st.info("No records found in the database. Add a student above!")
