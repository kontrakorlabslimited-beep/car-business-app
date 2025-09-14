
import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import os

# App title and logo
st.set_page_config(layout="wide")
st.image("abode_logo.png", width=100)
st.title("Abode Car Business Management App")

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# User credentials
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"}
}

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
    df = load_inventory()

    with st.form("vehicle_form"):
        vehicle_id = st.text_input("Vehicle ID")
        make = st.text_input("Make")
        model = st.text_input("Model")
        year = st.text_input("Year")
        purchase_price = st.number_input("Purchase Price (₦)", min_value=0)
        import_charges = st.number_input("Import Charges (₦)", min_value=0)
        repairs = st.number_input("Repairs (₦)", min_value=0)
        other_expenses = st.number_input("Other Expenses (₦)", min_value=0)
        exchange_rate = st.number_input("Exchange Rate", min_value=1.0, value=1000.0)
        sale_price = st.number_input("Sale Price (₦)", min_value=0)
        submitted = st.form_submit_button("Add Vehicle")

        if submitted:
            total_cost = purchase_price + import_charges + repairs + other_expenses
            profit_naira = sale_price - total_cost
            profit_dollar = profit_naira / exchange_rate
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
            st.success("Vehicle added successfully!")

    st.subheader("Inventory Summary")
    df = load_inventory()
    st.dataframe(df, use_container_width=True)

    st.subheader("Summary of Vehicles Sold by Make")
    if not df.empty:
        make_summary = df["Make"].value_counts().reset_index()
        make_summary.columns = ["Make", "Vehicles Sold"]
        st.dataframe(make_summary, use_container_width=True)

    st.subheader("Export Report")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"Abode_Inventory_Report_{timestamp}.csv"
    excel_filename = f"Abode_Inventory_Report_{timestamp}.xlsx"
    df.to_csv(csv_filename, index=False)
    df.to_excel(excel_filename, index=False)

    with open(csv_filename, "rb") as f:
        csv_data = f.read()
    with open(excel_filename, "rb") as f:
        excel_data = f.read()

    st.download_button("Download CSV", csv_data, file_name=csv_filename, mime="text/csv")
    st.download_button("Download Excel", excel_data, file_name=excel_filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Staff dashboard
def staff_dashboard():
    st.subheader("Inventory Summary")
    df = load_inventory()
    st.dataframe(df, use_container_width=True)

    st.subheader("Summary of Vehicles Sold by Make")
    if not df.empty:
        make_summary = df["Make"].value_counts().reset_index()
        make_summary.columns = ["Make", "Vehicles Sold"]
        st.dataframe(make_summary, use_container_width=True)

    st.subheader("Export Report")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"Abode_Inventory_Report_{timestamp}.csv"
    excel_filename = f"Abode_Inventory_Report_{timestamp}.xlsx"
    df.to_csv(csv_filename, index=False)
    df.to_excel(excel_filename, index=False)

    with open(csv_filename, "rb") as f:
        csv_data = f.read()
    with open(excel_filename, "rb") as f:
        excel_data = f.read()

    st.download_button("Download CSV", csv_data, file_name=csv_filename, mime="text/csv")
    st.download_button("Download Excel", excel_data, file_name=excel_filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Main app logic
if not st.session_state.logged_in:
    login()
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username} ({st.session_state.role})")
    logout()
    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        staff_dashboard()
