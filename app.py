
import streamlit as st
import pandas as pd
import os

# Constants
LOGO_FILE = "abode_logo.png"
DATA_FILE = "inventory.csv"

# User credentials and roles
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"}
}

# Load inventory from CSV
def load_inventory():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Vehicle ID", "Make", "Model", "Year", "Purchase Price (₦)", "Purchase Price ($)", "Sale Price (₦)", "Sale Price ($)", "Expenses (₦)", "Expenses ($)"])

# Save inventory to CSV
def save_inventory(df):
    df.to_csv(DATA_FILE, index=False)

# Login function
def login():
    st.title("Abode Car Business Management App")
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=150)
    else:
        st.info("Logo not found. Please upload 'abode_logo.png' to display branding.")

    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = USERS[username]["role"]
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# Logout function
def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""
    st.experimental_rerun()

# Admin interface
def admin_interface():
    st.sidebar.button("Logout", on_click=logout)
    st.title("Admin Dashboard")
    inventory = load_inventory()

    st.subheader("Add Vehicle")
    with st.form("add_vehicle_form"):
        vehicle_id = st.text_input("Vehicle ID")
        make = st.text_input("Make")
        model = st.text_input("Model")
        year = st.text_input("Year")
        purchase_naira = st.number_input("Purchase Price (₦)", min_value=0.0)
        purchase_dollar = st.number_input("Purchase Price ($)", min_value=0.0)
        sale_naira = st.number_input("Sale Price (₦)", min_value=0.0)
        sale_dollar = st.number_input("Sale Price ($)", min_value=0.0)
        expenses_naira = st.number_input("Expenses (₦)", min_value=0.0)
        expenses_dollar = st.number_input("Expenses ($)", min_value=0.0)
        submitted = st.form_submit_button("Add Vehicle")
        if submitted:
            new_row = {
                "Vehicle ID": vehicle_id,
                "Make": make,
                "Model": model,
                "Year": year,
                "Purchase Price (₦)": purchase_naira,
                "Purchase Price ($)": purchase_dollar,
                "Sale Price (₦)": sale_naira,
                "Sale Price ($)": sale_dollar,
                "Expenses (₦)": expenses_naira,
                "Expenses ($)": expenses_dollar
            }
            inventory = inventory.append(new_row, ignore_index=True)
            save_inventory(inventory)
            st.success("Vehicle added successfully.")

    st.subheader("Delete Vehicle")
    delete_id = st.text_input("Enter Vehicle ID to delete")
    if st.button("Delete Vehicle"):
        inventory = inventory[inventory["Vehicle ID"] != delete_id]
        save_inventory(inventory)
        st.success(f"Vehicle with ID '{delete_id}' deleted.")

    st.subheader("Inventory")
    st.dataframe(inventory, use_container_width=True)

    st.subheader("Profit/Loss Summary")
    inventory["Profit/Loss (₦)"] = inventory["Sale Price (₦)"] - (inventory["Purchase Price (₦)"] + inventory["Expenses (₦)"])
    inventory["Profit/Loss ($)"] = inventory["Sale Price ($)"] - (inventory["Purchase Price ($)"] + inventory["Expenses ($)"])
    st.dataframe(inventory[["Vehicle ID", "Make", "Model", "Profit/Loss (₦)", "Profit/Loss ($)"]], use_container_width=True)

# Staff interface
def staff_interface():
    st.sidebar.button("Logout", on_click=logout)
    st.title("Staff Dashboard")
    inventory = load_inventory()

    st.subheader("Inventory")
    st.dataframe(inventory, use_container_width=True)

    st.subheader("Profit/Loss Summary")
    inventory["Profit/Loss (₦)"] = inventory["Sale Price (₦)"] - (inventory["Purchase Price (₦)"] + inventory["Expenses (₦)"])
    inventory["Profit/Loss ($)"] = inventory["Sale Price ($)"] - (inventory["Purchase Price ($)"] + inventory["Expenses ($)"])
    st.dataframe(inventory[["Vehicle ID", "Make", "Model", "Profit/Loss (₦)", "Profit/Loss ($)"]], use_container_width=True)

# Main app logic
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

if st.session_state["logged_in"]:
    if st.session_state["role"] == "admin":
        admin_interface()
    else:
        staff_interface()
else:
    login()
