import streamlit as st
import pandas as pd
import os

# Constants
LOGO_FILE = "abode_logo.png"
DATA_FILE = "inventory.csv"
NAIRA_SYMBOL = "₦"
DOLLAR_SYMBOL = "$"
EXCHANGE_RATE = 1000  # 1 USD = 1000 NGN

# User credentials and roles
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"}
}

# Load or initialize inventory
def load_inventory():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Vehicle ID", "Make", "Model", "Year", "Purchase Price (₦)", "Import Charges (₦)", "Other Expenses (₦)", "Sale Price (₦)"])

def save_inventory(df):
    df.to_csv(DATA_FILE, index=False)

# Display logo
def display_logo():
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=150)
    else:
        st.markdown("### Abode Car Business Management App")

# Login screen
def login():
    st.title("Login")
    display_logo()
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = USERS[username]["role"]
        else:
            st.error("Invalid credentials")

# Logout
def logout():
    if st.sidebar.button("Logout"):
        st.session_state.clear()

# Admin dashboard
def admin_dashboard():
    st.title("Admin Dashboard")
    inventory = load_inventory()

    st.subheader("Add Vehicle")
    with st.form("add_vehicle"):
        vehicle_id = st.text_input("Vehicle ID")
        make = st.text_input("Make")
        model = st.text_input("Model")
        year = st.text_input("Year")
        purchase_price = st.number_input("Purchase Price (₦)", min_value=0)
        import_charges = st.number_input("Import Charges (₦)", min_value=0)
        other_expenses = st.number_input("Other Expenses (₦)", min_value=0)
        sale_price = st.number_input("Sale Price (₦)", min_value=0)
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
                "Sale Price (₦)": sale_price
            }
            inventory = inventory.append(new_row, ignore_index=True)
            save_inventory(inventory)
            st.success("Vehicle added successfully!")

    st.subheader("Delete Vehicle")
    delete_id = st.text_input("Enter Vehicle ID to delete")
    if st.button("Delete Vehicle"):
        inventory = inventory[inventory["Vehicle ID"] != delete_id]
        save_inventory(inventory)
        st.success(f"Vehicle with ID {delete_id} deleted.")

    st.subheader("Inventory")
    st.dataframe(inventory, use_container_width=True)

    st.subheader("Profit/Loss Summary")
    if not inventory.empty:
        inventory["Total Cost (₦)"] = inventory["Purchase Price (₦)"] + inventory["Import Charges (₦)"] + inventory["Other Expenses (₦)"]
        inventory["Profit/Loss (₦)"] = inventory["Sale Price (₦)"] - inventory["Total Cost (₦)"]
        inventory["Profit/Loss (USD)"] = inventory["Profit/Loss (₦)"] / EXCHANGE_RATE
        st.dataframe(inventory[["Vehicle ID", "Profit/Loss (₦)", "Profit/Loss (USD)"]], use_container_width=True)

# Staff dashboard
def staff_dashboard():
    st.title("Staff Dashboard")
    inventory = load_inventory()

    st.subheader("Inventory")
    st.dataframe(inventory, use_container_width=True)

    st.subheader("Profit/Loss Summary")
    if not inventory.empty:
        inventory["Total Cost (₦)"] = inventory["Purchase Price (₦)"] + inventory["Import Charges (₦)"] + inventory["Other Expenses (₦)"]
        inventory["Profit/Loss (₦)"] = inventory["Sale Price (₦)"] - inventory["Total Cost (₦)"]
        inventory["Profit/Loss (USD)"] = inventory["Profit/Loss (₦)"] / EXCHANGE_RATE
        st.dataframe(inventory[["Vehicle ID", "Profit/Loss (₦)", "Profit/Loss (USD)"]], use_container_width=True)

# Main app
def main():
    if "logged_in" not in st.session_state:
        login()
    else:
        logout()
        display_logo()
        st.markdown(f"### Welcome, {st.session_state['username'].capitalize()}!")
        if st.session_state["role"] == "admin":
            admin_dashboard()
        else:
            staff_dashboard()

if __name__ == "__main__":
    main()
