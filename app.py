
import streamlit as st
import pandas as pd
import os

# Constants
DATA_FILE = "inventory.csv"
LOGO_FILE = "abode_logo.png"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# Load or initialize inventory
def load_inventory():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Vehicle ID", "Make", "Model", "Year", "Purchase Price (₦)", "Import Charges (₦)", "Other Expenses (₦)", "Repairs (₦)", "Sale Price (₦)"])

def save_inventory(df):
    df.to_csv(DATA_FILE, index=False)

# Login system
def login():
    st.title("Abode Car Business Management App")
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=150)
    else:
        st.info("Logo not found. Upload 'abode_logo.png' to display it here.")

    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.role = "admin"
        elif username == "staff" and password == "staff123":
            st.session_state.logged_in = True
            st.session_state.role = "staff"
        else:
            st.error("Invalid credentials")

# Logout
def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.experimental_rerun()

# Admin dashboard
def admin_dashboard():
    st.title("Abode Car Business Management App")
    st.sidebar.button("Logout", on_click=logout)

    df = load_inventory()

    st.subheader("Add Vehicle")
    with st.form("add_vehicle"):
        vehicle_id = st.text_input("Vehicle ID")
        make = st.text_input("Make")
        model = st.text_input("Model")
        year = st.text_input("Year")
        purchase_price = st.number_input("Purchase Price (₦)", min_value=0.0)
        import_charges = st.number_input("Import Charges (₦)", min_value=0.0)
        other_expenses = st.number_input("Other Expenses (₦)", min_value=0.0)
        repairs = st.number_input("Repairs (₦)", min_value=0.0)
        sale_price = st.number_input("Sale Price (₦)", min_value=0.0)
        submitted = st.form_submit_button("Add Vehicle")
        if submitted:
            new_row = {
                "Vehicle ID": vehicle_id,
                "Make": make,
                "Model": model,
                "Year": year,
                "Purchase Price (₦)": purchase_price,
                "Import Charges (₦)": import_charges,
                "Other Expenses (₦)": other_expenses,
                "Repairs (₦)": repairs,
                "Sale Price (₦)": sale_price
            }
            df = df.append(new_row, ignore_index=True)
            save_inventory(df)
            st.success("Vehicle added successfully")

    st.subheader("Inventory")
    st.dataframe(df, use_container_width=True)

    st.subheader("Delete Vehicle")
    delete_id = st.text_input("Enter Vehicle ID to delete")
    if st.button("Delete"):
        df = df[df["Vehicle ID"] != delete_id]
        save_inventory(df)
        st.success(f"Vehicle with ID {delete_id} deleted")

    st.subheader("Profit/Loss Summary")
    if not df.empty:
        df["Total Cost (₦)"] = df["Purchase Price (₦)"] + df["Import Charges (₦)"] + df["Other Expenses (₦)"] + df["Repairs (₦)"]
        df["Profit/Loss (₦)"] = df["Sale Price (₦)"] - df["Total Cost (₦)"]
        df["Profit/Loss ($)"] = df["Profit/Loss (₦)"] / 1000
        st.dataframe(df[["Vehicle ID", "Make", "Model", "Year", "Total Cost (₦)", "Sale Price (₦)", "Profit/Loss (₦)", "Profit/Loss ($)"]], use_container_width=True)

# Staff dashboard
def staff_dashboard():
    st.title("Abode Car Business Management App")
    st.sidebar.button("Logout", on_click=logout)

    df = load_inventory()

    st.subheader("Inventory")
    st.dataframe(df, use_container_width=True)

    st.subheader("Profit/Loss Summary")
    if not df.empty:
        df["Total Cost (₦)"] = df["Purchase Price (₦)"] + df["Import Charges (₦)"] + df["Other Expenses (₦)"] + df["Repairs (₦)"]
        df["Profit/Loss (₦)"] = df["Sale Price (₦)"] - df["Total Cost (₦)"]
        df["Profit/Loss ($)"] = df["Profit/Loss (₦)"] / 1000
        st.dataframe(df[["Vehicle ID", "Make", "Model", "Year", "Total Cost (₦)", "Sale Price (₦)", "Profit/Loss (₦)", "Profit/Loss ($)"]], use_container_width=True)

# Main app
if not st.session_state.logged_in:
    login()
else:
    if st.session_state.role == "admin":
        admin_dashboard()
    elif st.session_state.role == "staff":
        staff_dashboard()
