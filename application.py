import streamlit as st
from streamlit_option_menu import option_menu
from db.connection import init_pool
from ui.students import students_page
from ui.dashboard import dashboard_page
from ui.queries import queries_page
from ui.tuition import tuition_page
from ui.enrollment import enroll_page

st.set_page_config(page_title="Student Information Manager", layout="wide")

# Initialize connection pool at startup
init_pool()

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Dashboard", "Students", "Queries", "Tuition", "Enrollments"],
        icons=["bar-chart", "person", "search", "receipt", "book"],
        menu_icon="cast",
        default_index=0
    )

if selected == "Dashboard":
    dashboard_page()
elif selected == "Students":
    students_page()
elif selected == "Queries":
    queries_page()
elif selected == "Tuition":
    tuition_page()
elif selected == "Enrollments":
    enroll_page()
