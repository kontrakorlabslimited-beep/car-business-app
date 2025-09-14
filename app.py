
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Dummy user database
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"}
}

# Load logo
def load_logo():
    if os.path.exists("abode_logo.png"):
        st.image("abode_logo.png", width=150)

# Login function
def login():
    st.title("Abode Car Business Management App")
    load_logo()
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

# Logout function
def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

# Admin dashboard
def admin_dashboard():
    st.title("Abode Car Business Management App")
    load_logo()
    st.sidebar.subheader(f"Logged in as: {st.session_state.username} (Admin)")
    logout()

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
    date = st.date_input("Date")

    if st.button("Add Vehicle"):
        new_data = {
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
            "Date": date
        }
        df = pd.read_csv("inventory.csv") if os.path.exists("inventory.csv") else pd.DataFrame()
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv("inventory.csv", index=False)
        st.success("Vehicle added successfully!")

    st.subheader("Inventory Summary")
    if os.path.exists("inventory.csv"):
        df = pd.read_csv("inventory.csv")
        df["Profit/Loss (₦)"] = df["Sale Price (₦)"] - df["Total Cost (₦)"]
        df["Profit/Loss ($)"] = df["Profit/Loss (₦)"] / df["Exchange Rate"]
        df["Status"] = df["Profit/Loss (₦)"].apply(lambda x: "Gain" if x > 0 else "Loss" if x < 0 else "Break-even")
        st.dataframe(df, use_container_width=True)

        st.subheader("Summary by Make")
        make_summary = df["Make"].value_counts().reset_index()
        make_summary.columns = ["Make", "Vehicles Sold"]
        st.dataframe(make_summary, use_container_width=True)

        st.subheader("Export Report")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = f"Abode_Inventory_Report_{timestamp}.csv"
        excel_file = f"Abode_Inventory_Report_{timestamp}.xlsx"
        df.to_csv(csv_file, index=False)
        df.to_excel(excel_file, index=False)

        with open(csv_file, "rb") as f:
            st.download_button("Download CSV", f, file_name=csv_file)

        with open(excel_file, "rb") as f:
            st.download_button("Download Excel", f, file_name=excel_file)

# Staff dashboard
def staff_dashboard():
    st.title("Abode Car Business Management App")
    load_logo()
    st.sidebar.subheader(f"Logged in as: {st.session_state.username} (Staff)")
    logout()

    st.subheader("Inventory Summary")
    if os.path.exists("inventory.csv"):
        df = pd.read_csv("inventory.csv")
        df["Profit/Loss (₦)"] = df["Sale Price (₦)"] - df["Total Cost (₦)"]
        df["Profit/Loss ($)"] = df["Profit/Loss (₦)"] / df["Exchange Rate"]
        df["Status"] = df["Profit/Loss (₦)"].apply(lambda x: "Gain" if x > 0 else "Loss" if x < 0 else "Break-even")
        st.dataframe(df, use_container_width=True)

        st.subheader("Summary by Make")
        make_summary = df["Make"].value_counts().reset_index()
        make_summary.columns = ["Make", "Vehicles Sold"]
        st.dataframe(make_summary, use_container_width=True)

# Main app logic
if st.session_state.logged_in:
    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        staff_dashboard()
else:
    login()
