# ui/enrollment.py
import streamlit as st
from db.queries import call_sp_register_course
from db.crud import read_enrollments

def enroll_page():
    st.header("Course Registration")
    sid = st.number_input("Student ID", min_value=3, step=1)
    cid = st.number_input("Course ID", min_value=1, step=1)
    semester = st.selectbox("Semester", ["Fall","Spring","Summer"])
    year = st.number_input("Academic Year", min_value=2000, max_value=2100, value=2025)
    if st.button("Register"):
        res = call_sp_register_course(sid, cid, semester, year)
        # show stored procedure messages if any
        if res:
            for result in res:
                st.write(result)
        else:
            st.success("Registration attempted. Check enrollments.")
    st.subheader("Current enrollments")
    st.dataframe(read_enrollments())
