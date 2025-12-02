# ui/students.py
import streamlit as st
from db import crud, setup
import pandas as pd
from utils.export import export_csv

def students_page():
    st.title("Students")

    ok, err = __connection_check()
    if not ok:
        st.error(f"DB connection failed: {err}")
        st.info("Check .env or DB server. You can create a local demo schema below.")
        if st.button("Create local demo schema"):
            try:
                setup.create_demo_schema()
                st.success("Demo schema created. Refresh the page.")
                st.rerun()
            except Exception as e:
                st.error(f"Failed: {e}")
        st.stop()

    missing = setup.find_missing_tables()
    if missing:
        st.warning(f"Missing expected tables: {', '.join(missing)}")
        if st.button("Create local demo schema"):
            setup.create_demo_schema()
            st.rerun()
        st.stop()

    action = st.radio("Action", ["View", "Add", "Edit", "Delete"])

    if action == "View":
        df, err = crud.read_students()
        if err:
            st.error("Read failed: " + err)
            return
        st.dataframe(df)
        if not df.empty:
            export_csv(df, "students_export.csv")

    elif action == "Add":
        st.subheader("Add student")
        with st.form("add"):
            student_id_opt = st.checkbox("Provide student_id manually (use only if schema has no AUTO_INCREMENT)")
            sid = None
            if student_id_opt:
                sid = st.number_input("Student ID", min_value=1, step=1)
            full_name = st.text_input("Full name")
            date_of_birth = st.date_input("Date of birth")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            email = st.text_input("Email")
            phone_number = st.text_input("Phone")
            address = st.text_area("Address")
            program_id = st.number_input("Program ID", min_value=0, step=1)
            enrollment_year = st.number_input("Enrollment year", min_value=1990, max_value=2100, value=2023)
            submitted = st.form_submit_button("Create")
            if submitted:
                ok, res = crud.create_student(full_name, date_of_birth, gender, email, phone_number, address, program_id, enrollment_year, student_id=sid if student_id_opt else None)
                if ok:
                    st.success(f"Created student id {res}")
                else:
                    st.error("Create failed: " + str(res))

    elif action == "Edit":
        df, err = crud.read_students()
        if err:
            st.error("Cannot load students: " + err)
            return
        if df.empty:
            st.info("No students to edit")
            return
        sid = st.selectbox("Select student id", df['student_id'].tolist())
        row = df[df['student_id'] == sid].iloc[0]
        with st.form("edit"):
            full_name = st.text_input("Full name", row['full_name'])
            date_of_birth = st.date_input("Date of birth", pd.to_datetime(row['date_of_birth']).date() if row['date_of_birth'] is not None else None)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male","Female","Other"].index(row.get('gender','Male')))
            email = st.text_input("Email", row.get('email',''))
            phone_number = st.text_input("Phone", row.get('phone_number',''))
            address = st.text_area("Address", row.get('address',''))
            program_id = st.number_input("Program ID", value=int(row.get('program_id') or 0))
            enrollment_year = st.number_input("Enrollment year", value=int(row.get('enrollment_year') or 2023))
            submitted = st.form_submit_button("Update")
            if submitted:
                ok, err = crud.update_student(sid, full_name, date_of_birth, gender, email, phone_number, address, program_id, enrollment_year)
                if ok:
                    st.success("Updated")
                else:
                    st.error("Update failed: " + str(err))

    elif action == "Delete":
        df, err = crud.read_students()
        if err:
            st.error("Cannot load students: " + err)
            return
        if df.empty:
            st.info("No students to delete")
            return
        sid = st.selectbox("Select student id to delete", df['student_id'].tolist())
        if st.button("Delete"):
            ok, err = crud.delete_student(sid)
            if ok:
                st.warning("Deleted")
            else:
                st.error("Delete failed: " + str(err))

def __connection_check():
    from db.connection import test_connection
    return test_connection()
