import streamlit as st
import pandas as pd
from auth import login, signup
from tracker import add_transaction, get_all_transactions, delete_all_transactions, update_transaction, get_by_month
from datetime import date

st.set_page_config(page_title="💸 Personal Finance Tracker", layout="wide")

if 'user' not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.markdown("""
        <h1 style='text-align: center;'>💸 Personal Finance Tracker</h1>
        <p style='text-align: center;'>Track your income and expenses effortlessly.</p>
    """, unsafe_allow_html=True)

    auth_choice = st.selectbox("Select Mode", ["Login", "Signup"])
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
    st.sidebar.title("🔧 Navigation")
    menu = st.sidebar.radio("Choose Action", ["Add", "View", "Edit", "Monthly", "Reset", "Logout"])

    if menu == "Add":
        st.title("➕ Add New Transaction")
        with st.form("add_form"):
            t_date = st.date_input("Date", value=date.today())
            t_type = st.radio("Type", ["Income", "Expense"], horizontal=True)
            t_category = st.text_input("Category")
            t_amount = st.number_input("Amount (₹)", min_value=0.0, step=0.5)
            submitted = st.form_submit_button("Add Transaction")
            if submitted:
                add_transaction(str(t_date), t_category, t_type, t_amount)
                st.success("Transaction added successfully!")

    elif menu == "View":
        st.title("📊 All Transactions")
        data = get_all_transactions()
        if data:
            df = pd.DataFrame(data, columns=["ID", "Date", "Category", "Type", "Amount"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No transactions to display.")

    elif menu == "Edit":
        st.title("✏️ Edit Transaction")
        data = get_all_transactions()
        if data:
            df = pd.DataFrame(data, columns=["ID", "Date", "Category", "Type", "Amount"])
            edit_row = st.selectbox("Select Transaction", df.index, format_func=lambda i: f"{df.loc[i, 'Date']} | {df.loc[i, 'Category']} | ₹{df.loc[i, 'Amount']}")
            selected = df.loc[edit_row]
            with st.form("edit_form"):
                e_date = st.date_input("Date", pd.to_datetime(selected["Date"]))
                e_type = st.radio("Type", ["Income", "Expense"], index=0 if selected["Type"] == "Income" else 1, horizontal=True)
                e_category = st.text_input("Category", selected["Category"])
                e_amount = st.number_input("Amount (₹)", value=float(selected["Amount"]))
                updated = st.form_submit_button("Update")
                if updated:
                    update_transaction(int(selected["ID"]), str(e_date), e_category, e_type, e_amount)
                    st.success("Transaction updated successfully!")
                    st.rerun()
        else:
            st.warning("No data available to edit.")

    elif menu == "Monthly":
        st.title("📆 View by Month")
        col1, col2 = st.columns(2)
        with col1:
            selected_month = st.selectbox("Month", list(range(1, 13)), format_func=lambda x: date(1900, x, 1).strftime('%B'))
        with col2:
            selected_year = st.selectbox("Year", list(range(2020, 2031)))

        if st.button("Show Monthly Transactions"):
            month_data = get_by_month(selected_month, selected_year)
            if month_data:
                df_month = pd.DataFrame(month_data, columns=["ID", "Date", "Category", "Type", "Amount"])
                st.dataframe(df_month, use_container_width=True)
            else:
                st.info("No transactions found for the selected month.")

    elif menu == "Reset":
        st.title("🗑️ Delete All Transactions")
        if st.button("Confirm Delete"):
            delete_all_transactions()
            st.success("All transactions deleted.")
            st.rerun()

    elif menu == "Logout":
        st.session_state.user = None
        st.rerun()
