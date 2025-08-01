import streamlit as st
import pandas as pd
from auth import login, signup
from tracker import add_transaction, get_all_transactions, delete_all_transactions, update_transaction, get_by_month
from datetime import date


st.set_page_config(page_title="Personal Finance Tracker", layout="wide")

# Set user session
if 'user' not in st.session_state:
    st.session_state.user = None
if 'nav' not in st.session_state:
    st.session_state.nav = "Home"

# Navbar buttons
def navbar():
    st.title("💰 Personal Finance Tracker")
    st.sidebar.header("📌 Navigation")

    if st.sidebar.button("🏠 Home"):
        st.session_state.nav = "Home"
    if st.sidebar.button("✏️ Edit Transaction"):
        st.session_state.nav = "Edit Transaction"
    if st.sidebar.button("📆 Filter by Month"):
        st.session_state.nav = "Filter by Month"
    if st.sidebar.button("🗑️ Reset Data"):
        st.session_state.nav = "Reset Data"

    st.sidebar.markdown("---")
    if st.sidebar.button("🔓 Logout"):
        st.session_state.user = None
        st.session_state.nav = "Home"
        st.rerun()

# Login or Signup
if not st.session_state.user:
    st.title("💰 Personal Finance Tracker")

    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = "Login"

    # Login / Signup toggle buttons
    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        if st.button("🔐 Login"):
            st.session_state.auth_mode = "Login"
    with btn_col2:
        if st.button("📝 Signup"):
            st.session_state.auth_mode = "Signup"

    st.markdown(f"### {st.session_state.auth_mode}")

    email = st.text_input("Email", key="email_input")
    password = st.text_input("Password", type="password", key="pass_input")
    if st.button("Submit"):
        if st.session_state.auth_mode == "Signup":
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

# Main UI
else:
    navbar()
    nav = st.session_state.nav
    user_email = st.session_state.user['email']

    if nav == "Home":
        st.header("➕ Add Transaction")
        with st.form("txn_form"):
            t_date = st.date_input("Date", value=date.today())
            t_type = st.selectbox("Type", ["Income", "Expense"])
            t_category = st.text_input("Category")
            t_amount = st.number_input("Amount (₹)", min_value=0.0, step=0.5)
            submitted = st.form_submit_button("Add")
            if submitted:
                add_transaction(user_email, str(t_date), t_category, t_type, t_amount)
                st.success("Transaction added!")

        st.header("📊 All Transactions")
        data = get_all_transactions(user_email)
        df = pd.DataFrame(data, columns=["Email", "Date", "Category", "Type", "Amount"])
        st.dataframe(df, use_container_width=True)

        if not df.empty:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Export as CSV", csv, "transactions.csv", "text/csv")

    elif nav == "Edit Transaction":
        st.header("✏️ Edit Transaction")
        data = get_all_transactions(user_email)
        df = pd.DataFrame(data, columns=["Email", "Date", "Category", "Type", "Amount"])
        if not df.empty:
            total_income = df[df["Type"] == "Income"]["Amount"].sum()
            total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
            balance = total_income - total_expense

            col1, col2, col3 = st.columns(3)
            col1.metric("💵 Total Income", f"₹{total_income:.2f}")
            col2.metric("💸 Total Expense", f"₹{total_expense:.2f}")
            col3.metric("🧾 Balance", f"₹{balance:.2f}")

            pie_data = df.groupby("Type")["Amount"].sum().reset_index()
            st.subheader("📈 Income vs Expense")
            st.plotly_chart({
                "data": [{
                    "labels": pie_data["Type"],
                    "values": pie_data["Amount"],
                    "type": "pie"
                }],
                "layout": {"margin": dict(t=0, b=0, l=0, r=0)}
            }, use_container_width=True)

        if len(df) > 0:
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
                    update_transaction(user_email, selected_txn["ID"], str(e_date), e_category, e_type, e_amount)
                    st.success("Transaction updated!")
                    st.rerun()
        else:
            st.warning("No transactions available to edit.")

    elif nav == "Filter by Month":
        st.header("📆 Filter by Month")
        month_col1, month_col2 = st.columns(2)
        with month_col1:
            selected_month = st.selectbox("Month", list(range(1, 13)))
        with month_col2:
            selected_year = st.selectbox("Year", list(range(2022, 2031)))

        if st.button("Show Transactions for Selected Month"):
            month_data = get_by_month(user_email, selected_month, selected_year)
            df_month = pd.DataFrame(month_data, columns=["Email", "Date", "Category", "Type", "Amount"])
            st.dataframe(df_month, use_container_width=True)

    elif nav == "Reset Data":
        st.header("🗑️ Reset All Data")
        if st.button("Delete All Transactions"):
            delete_all_transactions(user_email)
            st.success("All transactions deleted!")
            st.rerun()
