
import streamlit as st
import pandas as pd
import os

# File paths
DATA_FILE = "inventory_data.csv"
LOGO_FILE = "abode_logo.png"

# Sample user credentials and roles
USER_CREDENTIALS = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"}
}

# Load inventory data from CSV
def load_inventory():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Vehicle ID", "Make", "Model", "Year", "Purchase Price (₦)", "Purchase Price ($)", "Sale Price (₦)", "Sale Price ($)", "Expenses (₦)", "Expenses ($)"])

# Save inventory data to CSV
def save_inventory(df):
    df.to_csv(DATA_FILE, index=False)

# Welcome screen
def show_welcome_screen(username, role):
    st.image(LOGO_FILE, width=150)
    st.markdown(f"## Welcome, {username.capitalize()} ({role.capitalize()})")
    st.markdown("### Abode Car Business Management App")
    st.markdown("---")

# Login screen
def login():
    st.image(LOGO_FILE, width=150)
    st.title("Abode Car Business Management App")
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = USER_CREDENTIALS[username]["role"]
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# Main app interface
def main_app():
    show_welcome_screen(st.session_state["username"], st.session_state["role"])
    inventory = load_inventory()

    # Admin features
    if st.session_state["role"] == "admin":
        st.subheader("📋 Add Vehicle to Inventory")
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
                new_entry = {
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
                inventory = inventory.append(new_entry, ignore_index=True)
                save_inventory(inventory)
                st.success("Vehicle added successfully!")

        st.subheader("🗑️ Delete Vehicle from Inventory")
        delete_id = st.text_input("Enter Vehicle ID to Delete")
        if st.button("Delete Vehicle"):
            if delete_id in inventory["Vehicle ID"].values:
                inventory = inventory[inventory["Vehicle ID"] != delete_id]
                save_inventory(inventory)
                st.success(f"Vehicle ID {delete_id} deleted.")
            else:
                st.error("Vehicle ID not found.")

    # Inventory display
    st.subheader("📦 Vehicle Inventory")
    st.dataframe(inventory, use_container_width=True)

    # Profit/Loss Summary
    st.subheader("📊 Profit/Loss Summary")
    if not inventory.empty:
        inventory["Profit/Loss (₦)"] = inventory["Sale Price (₦)"] - (inventory["Purchase Price (₦)"] + inventory["Expenses (₦)"])
        inventory["Profit/Loss ($)"] = inventory["Sale Price ($)"] - (inventory["Purchase Price ($)"] + inventory["Expenses ($)"])
        st.dataframe(inventory[["Vehicle ID", "Make", "Model", "Profit/Loss (₦)", "Profit/Loss ($)"]], use_container_width=True)

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

# Streamlit session state initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Run app
if st.session_state["logged_in"]:
    main_app()
else:
    login()
