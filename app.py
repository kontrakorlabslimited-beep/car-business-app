import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Abode Car Business Management App", layout="wide")

LOGO_FILE = "abode_logo.png"
INVENTORY_FILE = "inventory.csv"

def load_inventory():
    try:
        return pd.read_csv(INVENTORY_FILE)
    except:
        return pd.DataFrame()

def save_inventory(df):
    df.to_csv(INVENTORY_FILE, index=False)

def login():
    st.image(LOGO_FILE, width=100)
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

def dashboard():
    st.sidebar.image(LOGO_FILE, width=100)
    st.sidebar.title("Abode Dashboard")
    logout()

    st.title("Abode Car Business Management App")

    df = load_inventory()

    st.subheader("Add Vehicle")
    with st.form("vehicle_form"):
        vehicle_id = st.text_input("Vehicle ID")
        make = st.text_input("Make")
        model = st.text_input("Model")
        year = st.number_input("Year", min_value=1980, max_value=2030, step=1)
        purchase_price = st.number_input("Purchase Price (₦)", min_value=0)
        iaa_fees = st.number_input("IAA Fees (₦)", min_value=0)
        dealer_fees = st.number_input("Dealer Fees (₦)", min_value=0)
        taxes = st.number_input("Taxes (₦)", min_value=0)
        towing_fees = st.number_input("Towing/Forklift Fees (₦)", min_value=0)
        demurrage = st.number_input("Demurrage (₦)", min_value=0)
        local_repairs = st.number_input("Local Repairs (₦)", min_value=0)
        other_expenses = st.number_input("Other Expenses (₦)", min_value=0)
        potential_sales_price = st.number_input("Potential Sales Price (₦)", min_value=0)
        sale_price = st.number_input("Sale Price (₦)", min_value=0)
        exchange_rate = st.number_input("Exchange Rate", min_value=1, value=1000)
        remarks = st.text_area("Remarks")
        submitted = st.form_submit_button("Add Vehicle")

    if submitted:
        total_cost = purchase_price + iaa_fees + dealer_fees + taxes + towing_fees + demurrage + local_repairs + other_expenses
        profit_loss = sale_price - total_cost
        profit_loss_usd = profit_loss / exchange_rate
        potential_profit = potential_sales_price - total_cost
        potential_profit_usd = potential_profit / exchange_rate
        status = "Gain" if profit_loss > 0 else "Loss" if profit_loss < 0 else "Break-even"

        new_row = pd.DataFrame([{
            "Vehicle ID": vehicle_id,
            "Make": make,
            "Model": model,
            "Year": year,
            "Purchase Price (₦)": purchase_price,
            "IAA Fees (₦)": iaa_fees,
            "Dealer Fees (₦)": dealer_fees,
            "Taxes (₦)": taxes,
            "Towing/Forklift Fees (₦)": towing_fees,
            "Demurrage (₦)": demurrage,
            "Local Repairs (₦)": local_repairs,
            "Other Expenses (₦)": other_expenses,
            "Total Cost (₦)": total_cost,
            "Sale Price (₦)": sale_price,
            "Exchange Rate": exchange_rate,
            "Profit/Loss (₦)": profit_loss,
            "Profit/Loss ($)": profit_loss_usd,
            "Potential Sales Price (₦)": potential_sales_price,
            "Potential Profit (₦)": potential_profit,
            "Potential Profit ($)": potential_profit_usd,
            "Remarks": remarks,
            "Status": status
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        save_inventory(df)
        st.success("Vehicle added successfully.")

    st.subheader("Inventory Summary")
    st.dataframe(df, use_container_width=True)

    st.subheader("Expense Summary")
    expense_columns = [
        "Purchase Price (₦)", "IAA Fees (₦)", "Dealer Fees (₦)", "Taxes (₦)",
        "Towing/Forklift Fees (₦)", "Demurrage (₦)", "Local Repairs (₦)", "Other Expenses (₦)"
    ]
    expense_summary = df[expense_columns].sum().reset_index()
    expense_summary.columns = ["Expense Type", "Total (₦)"]
    st.dataframe(expense_summary, use_container_width=True)

    st.subheader("Export Report")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"Abode_Inventory_Report_{timestamp}.csv"
    excel_filename = f"Abode_Inventory_Report_{timestamp}.xlsx"
    df.to_csv(csv_filename, index=False)
    df.to_excel(excel_filename, index=False)

    with open(csv_filename, "rb") as f:
        st.download_button("Download CSV", f, file_name=csv_filename)

    with open(excel_filename, "rb") as f:
        st.download_button("Download Excel", f, file_name=excel_filename)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    dashboard()
else:
    login()
