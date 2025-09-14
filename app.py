
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# App configuration
st.set_page_config(page_title="Abode Car Business Management App", layout="wide")

# Logo display
if os.path.exists("abode_logo.png"):
    st.image("abode_logo.png", width=120)

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Login function
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = "admin"
            st.experimental_rerun()
        elif username == "staff" and password == "staff123":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = "staff"
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

# Logout function
def logout():
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
            "Vehicle ID", "Make", "Model", "Year", "VIN",
            "Purchase Price (₦)", "IAA Fees (₦)", "Dealer Fees (₦)", "Taxes (₦)",
            "Towing/Forklift Fees (₦)", "Demurrage (₦)", "Local Repairs (₦)", "Other Expenses (₦)",
            "Total Cost (₦)", "Sale Price (₦)", "Profit/Loss (₦)", "Exchange Rate",
            "Profit/Loss ($)", "Potential Sales Price (₦)", "Potential Profit (₦)", "Potential Profit ($)",
            "Remarks"
        ])

# Save inventory
def save_inventory(df):
    df.to_csv("inventory.csv", index=False)

# Admin dashboard
def admin_dashboard():
    st.title("Abode Car Business Management Dashboard")
    st.sidebar.button("Logout", on_click=logout)

    df = load_inventory()

    st.subheader("Add New Vehicle")
    with st.form("vehicle_form"):
        vehicle_id = st.text_input("Vehicle ID")
        make = st.text_input("Make")
        model = st.text_input("Model")
        year = st.text_input("Year")
        vin = st.text_input("VIN")
        purchase_price = st.number_input("Purchase Price (₦)", min_value=0.0)
        iaa_fees = st.number_input("IAA Fees (₦)", min_value=0.0)
        dealer_fees = st.number_input("Dealer Fees (₦)", min_value=0.0)
        taxes = st.number_input("Taxes (₦)", min_value=0.0)
        towing_fees = st.number_input("Towing/Forklift Fees (₦)", min_value=0.0)
        demurrage = st.number_input("Demurrage (₦)", min_value=0.0)
        local_repairs = st.number_input("Local Repairs (₦)", min_value=0.0)
        other_expenses = st.number_input("Other Expenses (₦)", min_value=0.0)
        sale_price = st.number_input("Sale Price (₦)", min_value=0.0)
        exchange_rate = st.number_input("Exchange Rate", min_value=1.0, value=1000.0)
        potential_sales_price = st.number_input("Potential Sales Price (₦)", min_value=0.0)
        remarks = st.text_area("Remarks")

        submitted = st.form_submit_button("Add Vehicle")
        if submitted:
            total_cost = purchase_price + iaa_fees + dealer_fees + taxes + towing_fees + demurrage + local_repairs + other_expenses
            profit_loss = sale_price - total_cost
            profit_loss_usd = profit_loss / exchange_rate
            potential_profit = potential_sales_price - total_cost
            potential_profit_usd = potential_profit / exchange_rate

            new_row = pd.DataFrame([{
                "Vehicle ID": vehicle_id, "Make": make, "Model": model, "Year": year, "VIN": vin,
                "Purchase Price (₦)": purchase_price, "IAA Fees (₦)": iaa_fees, "Dealer Fees (₦)": dealer_fees,
                "Taxes (₦)": taxes, "Towing/Forklift Fees (₦)": towing_fees, "Demurrage (₦)": demurrage,
                "Local Repairs (₦)": local_repairs, "Other Expenses (₦)": other_expenses,
                "Total Cost (₦)": total_cost, "Sale Price (₦)": sale_price, "Profit/Loss (₦)": profit_loss,
                "Exchange Rate": exchange_rate, "Profit/Loss ($)": profit_loss_usd,
                "Potential Sales Price (₦)": potential_sales_price, "Potential Profit (₦)": potential_profit,
                "Potential Profit ($)": potential_profit_usd, "Remarks": remarks
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            save_inventory(df)
            st.success("Vehicle added successfully.")
            st.experimental_rerun()

    st.subheader("Inventory Summary")
    st.dataframe(df, use_container_width=True)

    st.subheader("Dashboard Summary")
    expense_columns = [
        "Purchase Price (₦)", "IAA Fees (₦)", "Dealer Fees (₦)", "Taxes (₦)",
        "Towing/Forklift Fees (₦)", "Demurrage (₦)", "Local Repairs (₦)", "Other Expenses (₦)"
    ]
    summary = df[expense_columns].sum().reset_index()
    summary.columns = ["Expense Type", "Total (₦)"]
    st.table(summary)

    st.subheader("Export Report")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"Abode_Inventory_Report_{timestamp}.csv"
    excel_filename = f"Abode_Inventory_Report_{timestamp}.xlsx"
    df.to_csv(csv_filename, index=False)
    df.to_excel(excel_filename, index=False)
    with open(csv_filename, "rb") as f:
        st.download_button("Download CSV Report", f, file_name=csv_filename)
    with open(excel_filename, "rb") as f:
        st.download_button("Download Excel Report", f, file_name=excel_filename)

# Staff dashboard
def staff_dashboard():
    st.title("Abode Car Business Management Dashboard")
    st.sidebar.button("Logout", on_click=logout)
    df = load_inventory()
    st.subheader("Inventory Summary")
    st.dataframe(df, use_container_width=True)

# Main app logic
if not st.session_state.logged_in:
    login()
else:
    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        staff_dashboard()
