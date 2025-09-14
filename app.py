import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(layout="wide")
LOGO_FILE = "abode_logo.png"
INVENTORY_FILE = "inventory.csv"

# Load inventory
if os.path.exists(INVENTORY_FILE):
    df = pd.read_csv(INVENTORY_FILE)
else:
    df = pd.DataFrame(columns=[
        "Vehicle ID", "Make", "Model", "Year", "Purchase Price (₦)", "IAA Fees (₦)", "Dealer Fees (₦)",
        "Taxes (₦)", "Towing/Forklift Fees (₦)", "Demurrage (₦)", "Local Repairs (₦)", "Other Expenses (₦)",
        "Total Cost (₦)", "Sale Price (₦)", "Profit/Loss (₦)", "Exchange Rate", "Profit/Loss ($)",
        "Potential Sales Price (₦)", "Potential Profit (₦)", "Potential Profit ($)", "Remarks"
    ])

# Display logo
if os.path.exists(LOGO_FILE):
    st.image(LOGO_FILE, width=100)

st.title("Abode Car Business Management App")

# Input form
st.subheader("Add Vehicle Transaction")
with st.form("vehicle_form"):
    cols = st.columns(5)
    vehicle_id = cols[0].text_input("Vehicle ID")
    make = cols[1].text_input("Make")
    model = cols[2].text_input("Model")
    year = cols[3].text_input("Year")
    exchange_rate = cols[4].number_input("Exchange Rate", value=1000)

    cols2 = st.columns(5)
    purchase_price = cols2[0].number_input("Purchase Price (₦)", value=0)
    iaa_fees = cols2[1].number_input("IAA Fees (₦)", value=0)
    dealer_fees = cols2[2].number_input("Dealer Fees (₦)", value=0)
    taxes = cols2[3].number_input("Taxes (₦)", value=0)
    towing_fees = cols2[4].number_input("Towing/Forklift Fees (₦)", value=0)

    cols3 = st.columns(5)
    demurrage = cols3[0].number_input("Demurrage (₦)", value=0)
    local_repairs = cols3[1].number_input("Local Repairs (₦)", value=0)
    other_expenses = cols3[2].number_input("Other Expenses (₦)", value=0)
    sale_price = cols3[3].number_input("Sale Price (₦)", value=0)
    potential_sale_price = cols3[4].number_input("Potential Sales Price (₦)", value=0)

    remarks = st.text_area("Remarks")

    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        total_cost = purchase_price + iaa_fees + dealer_fees + taxes + towing_fees + demurrage + local_repairs + other_expenses
        profit_loss = sale_price - total_cost
        profit_loss_usd = profit_loss / exchange_rate if exchange_rate else 0
        potential_profit = potential_sale_price - total_cost
        potential_profit_usd = potential_profit / exchange_rate if exchange_rate else 0

        new_row = {
            "Vehicle ID": vehicle_id, "Make": make, "Model": model, "Year": year,
            "Purchase Price (₦)": purchase_price, "IAA Fees (₦)": iaa_fees, "Dealer Fees (₦)": dealer_fees,
            "Taxes (₦)": taxes, "Towing/Forklift Fees (₦)": towing_fees, "Demurrage (₦)": demurrage,
            "Local Repairs (₦)": local_repairs, "Other Expenses (₦)": other_expenses,
            "Total Cost (₦)": total_cost, "Sale Price (₦)": sale_price, "Profit/Loss (₦)": profit_loss,
            "Exchange Rate": exchange_rate, "Profit/Loss ($)": profit_loss_usd,
            "Potential Sales Price (₦)": potential_sale_price, "Potential Profit (₦)": potential_profit,
            "Potential Profit ($)": potential_profit_usd, "Remarks": remarks
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(INVENTORY_FILE, index=False)
        st.success("Transaction added successfully.")

# Dashboard summary
st.subheader("Dashboard Summary")
expense_fields = ["Purchase Price (₦)", "IAA Fees (₦)", "Dealer Fees (₦)", "Taxes (₦)",
                  "Towing/Forklift Fees (₦)", "Demurrage (₦)", "Local Repairs (₦)", "Other Expenses (₦)"]
summary = {field: df[field].sum() for field in expense_fields}
summary_df = pd.DataFrame(list(summary.items()), columns=["Expense Type", "Total (₦)"])
st.dataframe(summary_df, use_container_width=True)

# Inventory summary
st.subheader("Inventory Summary")
st.dataframe(df, use_container_width=True)

# Export options
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
