import streamlit as st

# File-based Expense Tracker
FILE_NAME = "expenses.txt"

# Ensure file exists
try:
    open(FILE_NAME, "x").close()
except FileExistsError:
    pass

def add_expense(category, amount, date):
    """Add an expense to the file."""
    with open(FILE_NAME, "a") as file:
        file.write(f"{category},{amount},{date}\n")

def view_expenses():
    """Read and display expenses from the file."""
    try:
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()
        return [line.strip().split(",") for line in lines]
    except FileNotFoundError:
        return []

def delete_expense(index):
    """Delete an expense by its index."""
    expenses = view_expenses()
    if 0 <= index < len(expenses):
        expenses.pop(index)
        with open(FILE_NAME, "w") as file:
            for category, amount, date in expenses:
                file.write(f"{category},{amount},{date}\n")

def get_total_expenses():
    """Calculate the total amount spent."""
    return sum(float(amount) for _, amount, _ in view_expenses())

# Streamlit UI
st.title("Expense Tracker with File Persistence")
st.sidebar.header("Add Expense")

# Input Fields
category = st.sidebar.text_input("Category", placeholder="e.g., Food, Transport")
amount = st.sidebar.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
date = st.sidebar.date_input("Date")

# Add Expense Button
if st.sidebar.button("Add Expense"):
    if category and amount > 0:
        add_expense(category, amount, date)
        st.sidebar.success(f"Added ₹{amount:.2f} to {category}.")
    else:
        st.sidebar.warning("Please enter valid category and amount.")

# Display Expenses
st.header("Expense List")
expenses = view_expenses()

if expenses:
    for i, (category, amount, date) in enumerate(expenses):
        st.write(f"**{i+1}. {category}** - ₹{amount} (Date: {date})")
        if st.button(f"Delete {category} ({amount})", key=f"delete-{i}"):
            delete_expense(i)
            st.experimental_rerun()
else:
    st.info("No expenses recorded yet.")

# Total Expenses
st.header("Total Expenses")
total = get_total_expenses()
st.write(f"**Total Spent**: ₹{total:.2f}")

# Footer
st.write("---")
st.caption("Developed with ❤️ using Streamlit.")
