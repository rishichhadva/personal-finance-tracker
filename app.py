import streamlit as st
import pandas as pd
from auth import login, signup
from tracker import add_transaction, get_all_transactions, delete_all_transactions, update_transaction, get_by_month
from datetime import date

st.set_page_config(page_title="Personal Finance Tracker", layout="centered")

if 'user' not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.title("💰 Personal Finance Tracker")
    auth_choice = st.radio("Login / Signup", ["Login", "Signup"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if auth_choice == "Signup":
            if signup(email, password):
                st.success("Signup successful. Please login.")
            else:
                st.error("Signup failed.")
        else:
            user = login(email, password)
            if user:
                st.session_state.user = user
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Login failed.")
else:
    st.title("💰 Personal Finance Tracker")
    col1, col2 = st.columns([9, 1])
    with col1:
        st.markdown("## Dashboard")
    with col2:
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

    st.markdown("---")

    st.subheader("➕ Add Transaction")
    with st.form("txn_form"):
        t_date = st.date_input("Date", value=date.today())
        t_type = st.selectbox("Type", ["Income", "Expense"])
        t_category = st.text_input("Category")
        t_amount = st.number_input("Amount (₹)", min_value=0.0, step=0.5)
        submitted = st.form_submit_button("Add")
        if submitted:
            add_transaction(str(t_date), t_category, t_type, t_amount)
            st.success("Transaction added!")

    st.markdown("---")

    st.subheader("📊 All Transactions")
    data = get_all_transactions()
    if data:
        df = pd.DataFrame(data, columns=["ID", "Date", "Category", "Type", "Amount"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No transactions yet.")

    st.markdown("---")

    st.subheader("✏️ Edit Transaction")
    if data:
        df = pd.DataFrame(data, columns=["ID", "Date", "Category", "Type", "Amount"])
        df['Edit'] = df.index
        edit_row = st.selectbox("Select row to edit", df['Edit'])
        selected_txn = df.iloc[edit_row]

        with st.form("edit_form"):
            e_date = st.date_input("Date", pd.to_datetime(selected_txn["Date"]))
            e_type = st.selectbox("Type", ["Income", "Expense"], index=0 if selected_txn["Type"] == "Income" else 1)
            e_category = st.text_input("Category", selected_txn["Category"])
            e_amount = st.number_input("Amount (₹)", value=float(selected_txn["Amount"]), step=0.5)
            submit_edit = st.form_submit_button("Update Transaction")

            if submit_edit:
                update_transaction(int(selected_txn["ID"]), str(e_date), e_category, e_type, e_amount)
                st.success("Transaction updated!")
                st.rerun()
    else:
        st.info("No transactions available to edit.")

    st.markdown("---")

    st.subheader("📆 Filter by Month")
    col1, col2 = st.columns(2)
    with col1:
        selected_month = st.selectbox("Month", list(range(1, 13)))
    with col2:
        selected_year = st.selectbox("Year", list(range(2022, 2031)))

    if st.button("Show Transactions for Selected Month"):
        month_data = get_by_month(selected_month, selected_year)
        if month_data:
            df_month = pd.DataFrame(month_data, columns=["ID", "Date", "Category", "Type", "Amount"])
            st.dataframe(df_month, use_container_width=True)
        else:
            st.warning("No transactions found for selected month and year.")

    st.markdown("---")

    st.subheader("🗑️ Reset All Data")
    if st.button("Delete All Transactions"):
        delete_all_transactions()
        st.success("All transactions deleted!")
        st.rerun()
