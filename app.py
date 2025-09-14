
import streamlit as st
import pandas as pd
import os

# App title and logo
st.set_page_config(page_title="Abode Car Business Management App", layout="wide")
if os.path.exists("abode_logo.png"):
    st.image("abode_logo.png", width=120)
st.title("Abode Car Business Management App")

# Login credentials
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"}
}

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Login function
def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password")

# Load inventory
def load_inventory():
    if os.path.exists("inventory.csv"):
        return pd.read_csv("inventory.csv")
    else:
        return pd.DataFrame(columns=[
            "Vehicle ID", "Make", "Model", "Year", "Purchase Price (₦)", "Import Charges (₦)",
            "Repairs (₦)", "Other Expenses (₦)", "Total Cost (₦)", "Sale Price (₦)",
            "Exchange Rate", "Profit/Loss (₦)", "Profit/Loss ($)", "Status"
        ])

# Save inventory
def save_inventory(df):
    df.to_csv("inventory.csv", index=False)

# Export report
def export_report(df):
    df.to_csv("Abode_Inventory_Report.csv", index=False)
    try:
        import openpyxl
        df.to_excel("Abode_Inventory_Report.xlsx", index=False, engine="openpyxl")
        st.success("Report exported successfully.")
    except ImportError:
        st.warning("openpyxl not installed. Excel export skipped.")

# Admin dashboard
def admin_dashboard():
    st.subheader("Add Vehicle")
    vehicle_id = st.text_input("Vehicle ID")
    make = st.text_input("Make")
    model = st.text_input("Model")
    year = st.text_input("Year")
    purchase_price = st.number_input("Purchase Price (₦)", min_value=0.0, value=0.0)
    import_charges = st.number_input("Import Charges (₦)", min_value=0.0, value=0.0)
    repairs = st.number_input("Repairs (₦)", min_value=0.0, value=0.0)
    other_expenses = st.number_input("Other Expenses (₦)", min_value=0.0, value=0.0)
    sale_price = st.number_input("Sale Price (₦)", min_value=0.0, value=0.0)
    exchange_rate = st.number_input("Exchange Rate", min_value=1.0, value=1000.0)

    df = load_inventory()

    if st.button("Add Vehicle"):
        total_cost = purchase_price + import_charges + repairs + other_expenses
        profit_naira = sale_price - total_cost
        profit_dollar = profit_naira / exchange_rate if exchange_rate else 0
        status = "Gain" if profit_naira > 0 else "Loss" if profit_naira < 0 else "Break-even"
        new_row = pd.DataFrame([{
            "Vehicle ID": vehicle_id,
            "Make": make,
            "Model": model,
            "Year": year,
            "Purchase Price (₦)": purchase_price,
            "Import Charges (₦)": import_charges,
            "Repairs (₦)": repairs,
            "Other Expenses (₦)": other_expenses,
            "Total Cost (₦)": total_cost,
            "Sale Price (₦)": sale_price,
            "Exchange Rate": exchange_rate,
            "Profit/Loss (₦)": profit_naira,
            "Profit/Loss ($)": profit_dollar,
            "Status": status
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        save_inventory(df)
        st.success("Vehicle added successfully.")

    st.subheader("Inventory Summary")
    st.dataframe(df, use_container_width=True)

    st.subheader("Summary of Vehicles Sold by Make")
    make_summary = df["Make"].value_counts().reset_index()
    make_summary.columns = ["Make", "Number of Vehicles Sold"]
    st.table(make_summary)

    if st.button("Export Report"):
        export_report(df)

# Staff dashboard
def staff_dashboard():
    st.subheader("Inventory Summary")
    df = load_inventory()
    st.dataframe(df, use_container_width=True)

    st.subheader("Summary of Vehicles Sold by Make")
    make_summary = df["Make"].value_counts().reset_index()
    make_summary.columns = ["Make", "Number of Vehicles Sold"]
    st.table(make_summary)

# Logout
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.experimental_rerun()

# Main app logic
if not st.session_state.logged_in:
    login()
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username} ({st.session_state.role})")
    if st.sidebar.button("Logout"):
        logout()
    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        staff_dashboard()
