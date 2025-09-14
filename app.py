import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import os

# Load logo
if os.path.exists("abode_logo.png"):
    st.image("abode_logo.png", width=120)

st.title("Abode Car Business Management App")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# User credentials
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"}
}

# Login function
def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = USERS[username]["role"]
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# Logout button
def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.experimental_rerun()

# Load inventory
def load_inventory():
    if os.path.exists("inventory.csv"):
        return pd.read_csv("inventory.csv")
    else:
        return pd.DataFrame(columns=[
            "Vehicle ID", "Make", "Model", "Year", "Purchase Price (₦)",
            "Import Charges (₦)", "Repairs (₦)", "Other Expenses (₦)",
            "Total Cost (₦)", "Sale Price (₦)", "Exchange Rate",
            "Profit/Loss (₦)", "Profit/Loss ($)", "Status"
        ])

# Save inventory
def save_inventory(df):
    df.to_csv("inventory.csv", index=False)

# Admin dashboard
def admin_dashboard():
    st.subheader("Add Vehicle")
    vehicle_id = st.text_input("Vehicle ID")
    make = st.text_input("Make")
    model = st.text_input("Model")
    year = st.text_input("Year")
    purchase_price = st.number_input("Purchase Price (₦)", min_value=0)
    import_charges = st.number_input("Import Charges (₦)", min_value=0)
    repairs = st.number_input("Repairs (₦)", min_value=0)
    other_expenses = st.number_input("Other Expenses (₦)", min_value=0)
    total_cost = purchase_price + import_charges + repairs + other_expenses
    sale_price = st.number_input("Sale Price (₦)", min_value=0)
    exchange_rate = st.number_input("Exchange Rate", min_value=0.0, value=1000.0)

    if st.button("Add Vehicle"):
        df = load_inventory()
        profit_naira = sale_price - total_cost
        profit_dollar = profit_naira / exchange_rate if exchange_rate else 0
        status = "Gain" if profit_naira > 0 else "Loss" if profit_naira < 0 else "Break-even"
        new_row = {
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
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_inventory(df)
        st.success("Vehicle added successfully.")

    st.subheader("Inventory Summary")
    df = load_inventory()
    st.dataframe(df, use_container_width=True)

    st.subheader("Vehicles Sold by Make")
    make_summary = df["Make"].value_counts().reset_index()
    make_summary.columns = ["Make", "Count"]
    st.table(make_summary)

    st.subheader("Export Report")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"Abode_Inventory_Report_{timestamp}.csv"
    excel_filename = f"Abode_Inventory_Report_{timestamp}.xlsx"
    df.to_csv(csv_filename, index=False)
    try:
        df.to_excel(excel_filename, index=False)
    except:
        st.warning("Excel export failed. Please ensure openpyxl is installed.")

    with open(csv_filename, "rb") as f:
        st.download_button("Download CSV", f, file_name=csv_filename)

    if os.path.exists(excel_filename):
        with open(excel_filename, "rb") as f:
            st.download_button("Download Excel", f, file_name=excel_filename)

    logout()

# Staff dashboard
def staff_dashboard():
    st.subheader("Inventory Summary")
    df = load_inventory()
    st.dataframe(df, use_container_width=True)

    st.subheader("Vehicles Sold by Make")
    make_summary = df["Make"].value_counts().reset_index()
    make_summary.columns = ["Make", "Count"]
    st.table(make_summary)

    logout()

# Main app logic
if not st.session_state.logged_in:
    login()
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username} ({st.session_state.role})")
    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        staff_dashboard()
