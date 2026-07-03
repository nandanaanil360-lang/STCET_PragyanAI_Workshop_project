import streamlit as st
import sqlite3
import pandas as pd

# ----------------------------
# Database Connection
# ----------------------------

conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    department TEXT,
    semester INTEGER,
    email TEXT,
    phone TEXT
)
""")

conn.commit()

# ----------------------------
# Functions
# ----------------------------

def add_student(name, age, gender, dept, sem, email, phone):
    cursor.execute("""
    INSERT INTO students
    (name,age,gender,department,semester,email,phone)
    VALUES (?,?,?,?,?,?,?)
    """, (name, age, gender, dept, sem, email, phone))
    conn.commit()


def view_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()


def delete_student(student_id):
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()


def update_student(student_id, name, age, gender, dept, sem, email, phone):
    cursor.execute("""
    UPDATE students
    SET
    name=?,
    age=?,
    gender=?,
    department=?,
    semester=?,
    email=?,
    phone=?
    WHERE id=?
    """,
    (name, age, gender, dept, sem, email, phone, student_id))
    conn.commit()


def get_student(student_id):
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    return cursor.fetchone()


# ----------------------------
# UI
# ----------------------------

st.set_page_config(
    page_title="Student Record Management",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Record Management System")

menu = [
    "Home",
    "Add Student",
    "View Students",
    "Update Student",
    "Delete Student"
]

choice = st.sidebar.selectbox("Navigation", menu)

# ----------------------------
# HOME
# ----------------------------

if choice == "Home":

    st.header("Dashboard")

    data = view_students()

    total = len(data)

    col1, col2 = st.columns(2)

    col1.metric("Total Students", total)

    if total > 0:
        df = pd.DataFrame(
            data,
            columns=[
                "ID",
                "Name",
                "Age",
                "Gender",
                "Department",
                "Semester",
                "Email",
                "Phone"
            ]
        )

        col2.metric("Departments", df["Department"].nunique())

        st.subheader("Student Records")

        st.dataframe(df, use_container_width=True)

# ----------------------------
# ADD
# ----------------------------

elif choice == "Add Student":

    st.header("Add New Student")

    with st.form("student_form"):

        name = st.text_input("Student Name")

        age = st.number_input(
            "Age",
            min_value=15,
            max_value=60,
            value=18
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        department = st.selectbox(
            "Department",
            [
                "Computer Science",
                "Mechanical",
                "Civil",
                "Electrical",
                "Electronics",
                "MBA"
            ]
        )

        semester = st.selectbox(
            "Semester",
            [1,2,3,4,5,6,7,8]
        )

        email = st.text_input("Email")

        phone = st.text_input("Phone")

        submit = st.form_submit_button("Add Student")

        if submit:

            add_student(
                name,
                age,
                gender,
                department,
                semester,
                email,
                phone
            )

            st.success("Student Added Successfully")

# ----------------------------
# VIEW
# ----------------------------

elif choice == "View Students":

    st.header("Student List")

    data = view_students()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Name",
            "Age",
            "Gender",
            "Department",
            "Semester",
            "Email",
            "Phone"
        ]
    )

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        "students.csv",
        "text/csv"
    )

# ----------------------------
# UPDATE
# ----------------------------

elif choice == "Update Student":

    st.header("Update Student")

    data = view_students()

    ids = [x[0] for x in data]

    if len(ids) == 0:
        st.warning("No student records.")
    else:

        student_id = st.selectbox("Select Student ID", ids)

        student = get_student(student_id)

        with st.form("update_form"):

            name = st.text_input(
                "Name",
                student[1]
            )

            age = st.number_input(
                "Age",
                15,
                60,
                student[2]
            )

            gender = st.selectbox(
                "Gender",
                ["Male","Female","Other"],
                index=["Male","Female","Other"].index(student[3])
            )

            dept_list = [
                "Computer Science",
                "Mechanical",
                "Civil",
                "Electrical",
                "Electronics",
                "MBA"
            ]

            department = st.selectbox(
                "Department",
                dept_list,
                index=dept_list.index(student[4])
            )

            semester = st.selectbox(
                "Semester",
                [1,2,3,4,5,6,7,8],
                index=[1,2,3,4,5,6,7,8].index(student[5])
            )

            email = st.text_input(
                "Email",
                student[6]
            )

            phone = st.text_input(
                "Phone",
                student[7]
            )

            submit = st.form_submit_button("Update")

            if submit:

                update_student(
                    student_id,
                    name,
                    age,
                    gender,
                    department,
                    semester,
                    email,
                    phone
                )

                st.success("Student Updated Successfully")

# ----------------------------
# DELETE
# ----------------------------

elif choice == "Delete Student":

    st.header("Delete Student")

    data = view_students()

    ids = [x[0] for x in data]

    if len(ids) == 0:
        st.warning("No student records.")
    else:

        student_id = st.selectbox("Select Student", ids)

        student = get_student(student_id)

        st.write("### Student Details")

        st.write(f"**Name:** {student[1]}")
        st.write(f"**Department:** {student[4]}")
        st.write(f"**Semester:** {student[5]}")

        if st.button("Delete Student"):

            delete_student(student_id)

            st.success("Student Deleted Successfully")
