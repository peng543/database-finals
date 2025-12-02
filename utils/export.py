# utils/export.py
import streamlit as st

def export_csv(df, filename="export.csv"):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )
