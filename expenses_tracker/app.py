import streamlit as st
import pandas as pd
import datetime
import io
from database import create_db, add_expense, get_expenses
import sqlite3

DB_NAME = "expenses.db"

# ---------------- CONFIG ---------------- #
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

create_db()

st.title("💰 Expense Tracker")
st.caption("Smart personal finance & analytics system")

# ---------------- NAVIGATION ---------------- #
menu = st.sidebar.radio(
    "📌 Navigation",
    [
        "➕ Add Expense",
        "📋 View Expenses",
        "📊 Analytics",
        "💡 Budget & Insights",
        "⬇️ Export Data"
    ]
)

# ---------------- LOAD DATA ---------------- #
expenses = get_expenses()

if expenses:
    df = pd.DataFrame(
        expenses,
        columns=["ID", "Date", "Category", "Description", "Amount", "Payment"]
    )
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")
else:
    df = pd.DataFrame(
        columns=["ID", "Date", "Category", "Description", "Amount", "Payment", "Month"]
    )

# =====================================================
# ➕ ADD EXPENSE
# =====================================================
if menu == "➕ Add Expense":

    st.subheader("➕ Add New Expense")

    with st.form("add_form"):
        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("Date", datetime.date.today())
            category = st.selectbox(
                "Category",
                ["Food", "Transport", "Groceries", "Rent",
                 "Shopping", "Entertainment", "Bills", "Others"]
            )

        with col2:
            amount = st.number_input("Amount (₹)", min_value=0.0)
            payment = st.selectbox("Payment Mode", ["UPI", "Cash", "Card", "Net Banking"])

        description = st.text_input("Description")

        submit = st.form_submit_button("Save Expense")

        if submit:
            add_expense(str(date), category, description, amount, payment)
            st.success("✅ Expense added successfully")

# =====================================================
# 📋 VIEW + DELETE
# =====================================================
elif menu == "📋 View Expenses":

    st.subheader("📋 Expense History")

    if df.empty:
        st.info("No expenses available.")
    else:
        # Filters
        col1, col2, col3 = st.columns(3)

        with col1:
            cat_filter = st.multiselect(
                "Filter by Category",
                df["Category"].unique(),
                default=df["Category"].unique()
            )

        with col2:
            pay_filter = st.multiselect(
                "Payment Mode",
                df["Payment"].unique(),
                default=df["Payment"].unique()
            )

        with col3:
            search = st.text_input("Search description")

        filtered = df[
            (df["Category"].isin(cat_filter)) &
            (df["Payment"].isin(pay_filter))
        ]

        if search:
            filtered = filtered[
                filtered["Description"].str.contains(search, case=False, na=False)
            ]

        st.dataframe(
            filtered.sort_values("Date", ascending=False),
            use_container_width=True
        )

        # Delete
        st.divider()
        st.subheader("🗑️ Delete Expense")

        delete_id = st.number_input("Enter Expense ID", step=1)

        if st.button("Delete"):
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id=?", (delete_id,))
            conn.commit()
            conn.close()
            st.success("✅ Expense deleted. Refresh page.")

# =====================================================
# 📊 ANALYTICS
# =====================================================
elif menu == "📊 Analytics":

    st.subheader("📊 Expense Analytics")

    if df.empty:
        st.info("No data available.")
    else:
        total = df["Amount"].sum()

        c1, c2 = st.columns(2)
        c1.metric("💸 Total Expenses", f"₹{total:.0f}")
        c2.metric("📅 Months Tracked", df["Month"].nunique())

        st.divider()

        st.subheader("Category-wise Spending")
        cat = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        st.bar_chart(cat)

        st.subheader("Monthly Trend")
        monthly = df.groupby("Month")["Amount"].sum()
        st.line_chart(monthly)

# =====================================================
# 💡 BUDGET & INSIGHTS
# =====================================================
elif menu == "💡 Budget & Insights":

    st.subheader("💡 Budget & Smart Insights")

    monthly_budget = st.number_input(
        "Set Monthly Budget (₹)",
        value=15000.0,
        step=500.0
    )

    if not df.empty:
        current_month = pd.Timestamp.today().to_period("M")
        month_df = df[df["Month"] == current_month]

        spent = month_df["Amount"].sum()
        remaining = monthly_budget - spent

        c1, c2, c3 = st.columns(3)
        c1.metric("Budget", f"₹{monthly_budget:.0f}")
        c2.metric("Spent", f"₹{spent:.0f}")
        c3.metric("Remaining", f"₹{remaining:.0f}")

        st.progress(min(int((spent / monthly_budget) * 100), 100))

        st.divider()

        if remaining < 0:
            st.error("🚨 You exceeded your budget!")
        elif remaining < monthly_budget * 0.2:
            st.warning("⚠️ Budget running low.")
        else:
            st.success("✅ Budget under control")

        # Smart insights
        if not month_df.empty:
            top_cat = month_df.groupby("Category")["Amount"].sum().idxmax()
            st.info(f"📌 Highest spending category: **{top_cat}**")

# =====================================================
# ⬇️ EXPORT
# =====================================================
elif menu == "⬇️ Export Data":

    st.subheader("⬇️ Export Expenses")

    if df.empty:
        st.info("No data to export.")
    else:
        buffer = io.BytesIO()
        df.drop(columns=["Month"]).to_excel(
            buffer, index=False, engine="xlsxwriter"
        )

        st.download_button(
            "Download Excel File",
            buffer.getvalue(),
            file_name="expenses.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.caption("🚀 Expense Tracker | SQL • Analytics • Finance System")

