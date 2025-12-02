# in ui/tuition.py
import streamlit as st
from db.crud import insert_payment, read_tuition_by_feeid  # implement these helpers
def tuition_page():
    st.header("Record Payment")
    fee = st.number_input("Fee ID", min_value=31, step=1)
    amount = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f")
    if st.button("Record Payment"):
        ok, err = insert_payment(fee, amount)
        if ok:
            st.success("Payment recorded. Trigger should update tuition fee.")
            df = read_tuition_by_feeid(fee)
            st.table(df.T)
        else:
            st.error("Payment failed: " + err)
