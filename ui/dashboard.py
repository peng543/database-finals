# ui/dashboard.py
import streamlit as st
import matplotlib.pyplot as plt
from db.connection import get_connection
from db import setup
import pandas as pd

def dashboard_page():
    st.title("Dashboard")

    ok, err = __connection_check()
    if not ok:
        st.error("DB connection failed: " + str(err))
        return

    missing = setup.find_missing_tables()
    if missing:
        st.warning(f"Missing tables: {', '.join(missing)} — dashboard limited")

    # Students per program
    try:
        conn = get_connection()
        q1 = ("SELECT p.program_id, p.program_name, COUNT(s.student_id) AS students_count "
              "FROM PROGRAM p LEFT JOIN STUDENT s ON p.program_id = s.program_id "
              "GROUP BY p.program_id, p.program_name ORDER BY students_count DESC")
        df_prog = pd.read_sql(q1, conn)
        # outstanding tuition per program
        q2 = ("SELECT p.program_id, p.program_name, SUM(COALESCE(tf.total_amount,0) - COALESCE(tf.amount_paid,0)) AS outstanding "
              "FROM PROGRAM p "
              "LEFT JOIN STUDENT s ON p.program_id = s.program_id "
              "LEFT JOIN TUITION_FEE tf ON s.student_id = tf.student_id "
              "GROUP BY p.program_id, p.program_name")
        df_out = pd.read_sql(q2, conn)
        conn.close()
    except Exception as e:
        st.error("Failed to load dashboard data: " + str(e))
        return

    if not df_prog.empty:
        st.subheader("Students per Program")
        fig, ax = plt.subplots()
        ax.bar(df_prog['program_name'], df_prog['students_count'])
        ax.set_xticklabels(df_prog['program_name'], rotation=30, ha='right')
        st.pyplot(fig)

    if not df_out.empty:
        st.subheader("Outstanding tuition by program")
        fig2, ax2 = plt.subplots()
        ax2.bar(df_out['program_name'], df_out['outstanding'])
        ax2.set_xticklabels(df_out['program_name'], rotation=30, ha='right')
        st.pyplot(fig2)

def __connection_check():
    from db.connection import test_connection
    return test_connection()
