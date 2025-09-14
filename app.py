import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")

# Load inventory
inventory_file = "inventory.csv"
if os.path.exists(inventory_file):
    df = pd.read_csv(inventory_file)
else:
    df = pd.DataFrame(columns=[
        "Vehicle ID", "Make", "Model", "Year", "Purchase Price (₦)", "Import Charges (₦)",
        "Repairs (₦)", "Other Expenses (₦)", "Exchange Rate", "Sale Price (₦)",
        "Total Cost (₦)", "Profit/Loss (₦)", "Profit/Loss ($)", "Status"
    ])

# Logo and title
if os.path.exists("abode_logo.png"):
    st.image("abode_logo.png", width=150)
st.title("Abode Car Business Management App")

# Input form
st.header("Add Vehicle Information")
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
            "Total Cost (₦)": total_cost,
            "Profit/Loss (₦)": profit_naira,
            "Profit/Loss ($)": profit_dollar,
            "Status": status
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(inventory_file, index=False)
        st.success("Vehicle added successfully!")

# Display inventory
st.header("Inventory Summary")
styled_df = df.style.applymap(
    lambda val: "background-color: lightgreen" if val == "Gain" else
                "background-color: lightcoral" if val == "Loss" else
                "background-color: lightgray",
    subset=["Status"]
)
st.dataframe(styled_df, use_container_width=True)

# Charts
st.header("Charts by Vehicle Make")
if not df.empty:
    fig1, ax1 = plt.subplots()
    df.groupby("Make")["Profit/Loss (₦)"].sum().plot(kind="bar", ax=ax1, title="Total Profit/Loss by Make")
    fig1.tight_layout()
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    df["Make"].value_counts().plot(kind="bar", ax=ax2, title="Number of Vehicles by Make")
    fig2.tight_layout()
    st.pyplot(fig2)

# Export options
st.header("Export Report")
csv_export = df.to_csv(index=False).encode("utf-8")
df.to_excel("Abode_Inventory_Report.xlsx", index=False)
st.download_button("Download CSV", csv_export, "Abode_Inventory_Report.csv", "text/csv")
st.download_button("Download Excel", open("Abode_Inventory_Report.xlsx", "rb").read(), "Abode_Inventory_Report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
