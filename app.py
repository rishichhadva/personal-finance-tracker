import streamlit as st
from tracker import (
    connect_db, add_transaction, get_all_transactions,
    get_summary, get_categories, get_by_category, get_expense_by_category
)
import pandas as pd
import matplotlib.pyplot as plt
from auth import login, signup

st.title("🔐 Login to Personal Finance Tracker")

choice = st.selectbox("Login or Sign Up?", ["Login", "Sign Up"])
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if choice == "Sign Up":
    if st.button("Create Account"):
        if signup(email, password):
            st.success("Account created!")
        else:
            st.error("Error creating account.")

if choice == "Login":
    if st.button("Login"):
        user = login(email, password)
        if user:
            st.success("Logged in successfully!")
            # Show main app
        else:
            st.error("Invalid credentials.")

st.set_page_config(page_title="Personal Finance Tracker", layout="centered")
connect_db()

st.title("📊 Personal Finance Tracker")

# --- Add Transaction ---
st.header("➕ Add Transaction")
with st.form("add_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date")
        t_type = st.selectbox("Type", ["Income", "Expense"])
    with col2:
        category = st.text_input("Category")
        amount = st.number_input("Amount (₹)", min_value=0.0, step=0.5)
    submitted = st.form_submit_button("Add Transaction")
    if submitted and category and amount > 0:
        add_transaction(str(date), category, t_type, amount)
        st.success("Transaction added!")

# --- Summary ---
st.header("📈 Summary")
income, expense, net = get_summary()
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{income:.2f}")
col2.metric("Total Expense", f"₹{expense:.2f}")
col3.metric("Net Savings", f"₹{net:.2f}")

# --- All Transactions ---
st.header("📄 All Transactions")
all_data = get_all_transactions()
df = pd.DataFrame(all_data, columns=["Date", "Category", "Type", "Amount"])
st.dataframe(df, use_container_width=True)
st.download_button(
    label="📥 Download as CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='transactions.csv',
    mime='text/csv'
)

# --- Filter by Category ---
st.header("🔍 Filter by Category")
categories = get_categories()
if categories:
    selected = st.selectbox("Select a category", categories)
    filtered = get_by_category(selected)
    df_filtered = pd.DataFrame(filtered, columns=["Date", "Category", "Type", "Amount"])
    st.dataframe(df_filtered, use_container_width=True)

# --- Pie Chart ---
st.header("🧁 Expense Breakdown (Pie Chart)")
data = get_expense_by_category()
if data:
    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.info("No expense data to display.")
