
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
LOGO_FILE = "abode_logo.png"

def load_inventory():
    try:
        df = pd.read_csv("inventory.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "Vehicle ID", "Make", "Model", "Year",
            "Purchase Price (₦)", "Import Charges (₦)", "Repairs (₦)", "Other Expenses (₦)",
            "Total Cost (₦)", "Sale Price (₦)", "Exchange Rate",
            "Profit/Loss (₦)", "Profit/Loss ($)", "Status"
        ])
    return df

def save_inventory(df):
    df.to_csv("inventory.csv", index=False)

def calculate_profit_loss(row):
    total_cost = row["Purchase Price (₦)"] + row["Import Charges (₦)"] + row["Repairs (₦)"] + row["Other Expenses (₦)"]
    profit_naira = row["Sale Price (₦)"] - total_cost
    profit_dollar = profit_naira / row["Exchange Rate"] if row["Exchange Rate"] else 0
    status = "Gain" if profit_naira > 0 else "Loss" if profit_naira < 0 else "Break-even"
    return total_cost, profit_naira, profit_dollar, status

def main():
    st.image(LOGO_FILE, width=120)
    st.title("Abode Car Business Management App")

    role = st.sidebar.selectbox("Select Role", ["Admin", "Staff"])
    if role == "Admin":
        st.subheader("Add Vehicle")
        with st.form("vehicle_form"):
            vehicle_id = st.text_input("Vehicle ID")
            make = st.text_input("Make")
            model = st.text_input("Model")
            year = st.number_input("Year", min_value=1980, max_value=2030, step=1)
            purchase_price = st.number_input("Purchase Price (₦)", min_value=0)
            import_charges = st.number_input("Import Charges (₦)", min_value=0)
            repairs = st.number_input("Repairs (₦)", min_value=0)
            other_expenses = st.number_input("Other Expenses (₦)", min_value=0)
            sale_price = st.number_input("Sale Price (₦)", min_value=0)
            exchange_rate = st.number_input("Exchange Rate", min_value=1.0, value=1000.0)
            submitted = st.form_submit_button("Add Vehicle")

        if submitted:
            df = load_inventory()
            total_cost, profit_naira, profit_dollar, status = calculate_profit_loss({
                "Purchase Price (₦)": purchase_price,
                "Import Charges (₦)": import_charges,
                "Repairs (₦)": repairs,
                "Other Expenses (₦)": other_expenses,
                "Sale Price (₦)": sale_price,
                "Exchange Rate": exchange_rate
            })
            new_row = {
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
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_inventory(df)
            st.success("Vehicle added successfully.")

    st.subheader("Inventory Summary")
    df = load_inventory()
    st.dataframe(df, use_container_width=True)

    st.subheader("Summary of Vehicles Sold by Make")
    if not df.empty:
        make_summary = df["Make"].value_counts().reset_index()
        make_summary.columns = ["Make", "Count"]
        st.table(make_summary)

    st.subheader("Export Report")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"Abode_Inventory_Report_{timestamp}.csv"
    excel_filename = f"Abode_Inventory_Report_{timestamp}.xlsx"
    df.to_csv(csv_filename, index=False)
    try:
        import openpyxl
        df.to_excel(excel_filename, index=False)
        with open(excel_filename, "rb") as f:
            st.download_button("Download Excel", f, file_name=excel_filename)
    except ImportError:
        st.warning("Excel export requires openpyxl. Please install it to enable Excel downloads.")
    with open(csv_filename, "rb") as f:
        st.download_button("Download CSV", f, file_name=csv_filename)

if __name__ == "__main__":
    main()
