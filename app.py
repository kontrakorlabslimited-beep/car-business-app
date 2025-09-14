
import streamlit as st
import pandas as pd
import os
from datetime import datetime

LOGO_FILE = "abode_logo.png"
INVENTORY_FILE = "inventory.csv"

# Load inventory
if os.path.exists(INVENTORY_FILE):
    df = pd.read_csv(INVENTORY_FILE)
else:
    df = pd.DataFrame(columns=[
        "Vehicle ID", "Make", "Model", "Year", "Purchase Price (₦)", "Import Charges (₦)",
        "Repairs (₦)", "Other Expenses (₦)", "Exchange Rate", "Sale Price (₦)",
        "Profit/Loss (₦)", "Profit/Loss ($)", "Status"
    ])

st.set_page_config(layout="wide")
if os.path.exists(LOGO_FILE):
    st.image(LOGO_FILE, width=150)
st.title("Abode Car Business Management App")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")

if not st.session_state.logged_in:
    login()
else:
    st.subheader("Add Vehicle")
    with st.form("vehicle_form"):
        vehicle_id = st.text_input("Vehicle ID")
        make = st.text_input("Make")
        model = st.text_input("Model")
        year = st.text_input("Year")
        purchase_price = st.number_input("Purchase Price (₦)", min_value=0)
        import_charges = st.number_input("Import Charges (₦)", min_value=0)
        repairs = st.number_input("Repairs (₦)", min_value=0)
        other_expenses = st.number_input("Other Expenses (₦)", min_value=0)
        exchange_rate = st.number_input("Exchange Rate", min_value=0.0, value=1000.0)
        sale_price = st.number_input("Sale Price (₦)", min_value=0)
        submitted = st.form_submit_button("Add Vehicle")

        if submitted:
            total_cost = purchase_price + import_charges + repairs + other_expenses
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
                "Exchange Rate": exchange_rate,
                "Sale Price (₦)": sale_price,
                "Profit/Loss (₦)": profit_naira,
                "Profit/Loss ($)": profit_dollar,
                "Status": status
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(INVENTORY_FILE, index=False)
            st.success("Vehicle added successfully!")

    st.subheader("Inventory Summary")
    st.dataframe(df, use_container_width=True)

    st.subheader("Summary of Vehicles Sold by Make")
    if not df.empty:
        make_summary = df["Make"].value_counts().reset_index()
        make_summary.columns = ["Make", "Number Sold"]
        st.table(make_summary)

    st.subheader("Export Report")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"Abode_Inventory_Report_{timestamp}.csv"
    excel_filename = f"Abode_Inventory_Report_{timestamp}.xlsx"

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv_data, file_name=csv_filename, mime="text/csv")

    try:
        import openpyxl
        from io import BytesIO
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, engine="openpyxl")
        st.download_button("Download Excel", data=excel_buffer.getvalue(), file_name=excel_filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except ImportError:
        st.warning("Excel export requires 'openpyxl'. Please install it to enable Excel downloads.")

    st.info("✅ Report exported successfully. Check your Downloads folder.")
