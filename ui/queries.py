# ui/queries.py
import streamlit as st
import pandas as pd
from db.connection import get_connection
from db import setup
from db.queries import read_view, call_sp_register_course, call_sp_semester_revenue_report
from utils.export import export_csv

def queries_page():
    st.title("Queries")

    ok, err = __connection_check()
    if not ok:
        st.error("DB connection failed: " + str(err))
        return

    missing = setup.find_missing_tables()
    if missing:
        st.warning("Missing tables: " + ", ".join(missing))

    qmap = {
        "Students by program": "SELECT program_id, COUNT(*) AS student_count FROM STUDENT GROUP BY program_id",
        "Students by enrollment year": "SELECT enrollment_year, COUNT(*) AS student_count FROM STUDENT GROUP BY enrollment_year ORDER BY enrollment_year DESC",
        "Outstanding tuition": ("SELECT s.student_id, s.full_name, p.program_name, tf.total_amount, tf.amount_paid, "
                                "(tf.total_amount - tf.amount_paid) AS outstanding "
                                "FROM TUITION_FEE tf JOIN STUDENT s ON tf.student_id = s.student_id "
                                "LEFT JOIN PROGRAM p ON s.program_id = p.program_id "
                                "WHERE (tf.total_amount - tf.amount_paid) > 0")
    }

    choice = st.selectbox("Choose a query", list(qmap.keys()))
    if st.button("Run"):
        try:
            conn = get_connection()
            df = pd.read_sql(qmap[choice], conn)
            conn.close()
            st.dataframe(df)
            if not df.empty:
                export_csv(df, filename=f"{choice.replace(' ','_')}.csv")
        except Exception as e:
            st.error("Query failed: " + str(e))

def __connection_check():
    from db.connection import test_connection
    return test_connection()


def read_view(view_name, limit=None):
    return read_view(view_name, limit)

def call_sp_register_course(student_id, course_id, semester, academic_year):
    return call_sp_register_course(student_id, course_id, semester, academic_year)

def call_sp_semester_revenue_report(year, semester):
    return call_sp_semester_revenue_report(year, semester)
