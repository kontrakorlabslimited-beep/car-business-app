
import streamlit as st
import pandas as pd
from datetime import datetime

# Logo display
try:
    st.image("abode_logo.png", width=150)
except:
    st.write("Abode Car Business Management App")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Login credentials
USER_CREDENTIALS = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"}
}

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = USER_CREDENTIALS[username]["role"]
        else:
            st.error("Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

def load_inventory():
    try:
        return pd.read_csv("inventory.csv")
    except:
        return pd.DataFrame(columns=[
            "Vehicle ID", "Make", "Model", "Year", "VIN", "Purchase Price (₦)",
            "IAA Fees (₦)", "Dealer Fees (₦)", "Taxes (₦)", "Towing/Forklift Fees (₦)",
            "Demurrage (₦)", "Local Repairs (₦)", "Other Expenses (₦)",
            "Total Cost (₦)", "Sale Price (₦)", "Profit/Loss (₦)", "Exchange Rate",
            "Profit/Loss ($)", "Potential Sales Price (₦)", "Potential Profit (₦)",
            "Potential Profit ($)", "Remarks"
        ])

def save_inventory(df):
    df.to_csv("inventory.csv", index=False)

def admin_dashboard():
    st.title("Abode Car Business Management App")
    st.subheader(f"Welcome, {st.session_state.username} (Admin)")
    if st.sidebar.button("Logout"):
        logout()

    df = load_inventory()

    st.subheader("Add Vehicle")
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

            new_row = {
                "Vehicle ID": vehicle_id,
                "Make": make,
                "Model": model,
                "Year": year,
                "VIN": vin,
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
                "Profit/Loss (₦)": profit_loss,
                "Exchange Rate": exchange_rate,
                "Profit/Loss ($)": profit_loss_usd,
                "Potential Sales Price (₦)": potential_sales_price,
                "Potential Profit (₦)": potential_profit,
                "Potential Profit ($)": potential_profit_usd,
                "Remarks": remarks
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_inventory(df)
            st.success("Vehicle added successfully.")

    st.subheader("Inventory Summary")
    st.dataframe(df, use_container_width=True)

    st.subheader("Dashboard Summary")
    expense_columns = [
        "Purchase Price (₦)", "IAA Fees (₦)", "Dealer Fees (₦)", "Taxes (₦)",
        "Towing/Forklift Fees (₦)", "Demurrage (₦)", "Local Repairs (₦)", "Other Expenses (₦)"
    ]
    summary = df[expense_columns].sum().to_frame(name="Total (₦)")
    st.dataframe(summary)

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

def staff_dashboard():
    st.title("Abode Car Business Management App")
    st.subheader(f"Welcome, {st.session_state.username} (Staff)")
    if st.sidebar.button("Logout"):
        logout()

    df = load_inventory()
    st.subheader("Inventory Summary")
    st.dataframe(df, use_container_width=True)

if st.session_state.logged_in:
    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        staff_dashboard()
else:
    login()
