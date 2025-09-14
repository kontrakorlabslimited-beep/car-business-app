import streamlit as st
import pandas as pd
import os
from PIL import Image

# Load logo
if os.path.exists("abode_logo.png"):
    st.image("abode_logo.png", width=120)

st.title("Abode Car Business Management App")

# Login system
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.role = "admin"
        elif username == "staff" and password == "staff123":
            st.session_state.logged_in = True
            st.session_state.role = "staff"
        else:
            st.error("Invalid credentials")

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.experimental_rerun()

def load_inventory():
    if os.path.exists("inventory.csv"):
        return pd.read_csv("inventory.csv")
    else:
        return pd.DataFrame(columns=[
            "Vehicle ID", "Make", "Model", "Year", "Purchase Price (₦)", "Import Charges (₦)",
            "Repairs (₦)", "Other Expenses (₦)", "Exchange Rate", "Sale Price (₦)",
            "Profit/Loss (₦)", "Profit/Loss ($)", "Status"
        ])

def save_inventory(df):
    df.to_csv("inventory.csv", index=False)

def calculate_profit(row):
    total_cost = row["Purchase Price (₦)"] + row["Import Charges (₦)"] + row["Repairs (₦)"] + row["Other Expenses (₦)"]
    profit_naira = row["Sale Price (₦)"] - total_cost
    profit_dollar = profit_naira / row["Exchange Rate"] if row["Exchange Rate"] else 0
    if profit_naira > 0:
        status = "Gain"
    elif profit_naira < 0:
        status = "Loss"
    else:
        status = "Break-even"
    return pd.Series([profit_naira, profit_dollar, status])

def admin_dashboard():
    st.subheader("Admin Dashboard")
    df = load_inventory()

    st.subheader("Add Vehicle")
    with st.form("add_vehicle"):
        vehicle_id = st.text_input("Vehicle ID")
        make = st.text_input("Make")
        model = st.text_input("Model")
        year = st.number_input("Year", min_value=1980, max_value=2030, step=1)
        purchase_price = st.number_input("Purchase Price (₦)", min_value=0.0)
        import_charges = st.number_input("Import Charges (₦)", min_value=0.0)
        repairs = st.number_input("Repairs (₦)", min_value=0.0)
        other_expenses = st.number_input("Other Expenses (₦)", min_value=0.0)
        exchange_rate = st.number_input("Exchange Rate", min_value=1.0, value=1000.0)
        sale_price = st.number_input("Sale Price (₦)", min_value=0.0)
        submitted = st.form_submit_button("Add Vehicle")
        if submitted:
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
                "Sale Price (₦)": sale_price
            }
            profit_loss = calculate_profit(pd.Series(new_row))
            new_row["Profit/Loss (₦)"] = profit_loss[0]
            new_row["Profit/Loss ($)"] = profit_loss[1]
            new_row["Status"] = profit_loss[2]
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_inventory(df)
            st.success("Vehicle added successfully.")

    st.subheader("Inventory Summary")
    st.dataframe(df)

    st.subheader("Delete Vehicle")
    delete_id = st.text_input("Enter Vehicle ID to delete")
    if st.button("Delete"):
        df = df[df["Vehicle ID"] != delete_id]
        save_inventory(df)
        st.success(f"Vehicle ID {delete_id} deleted.")

    st.subheader("Export Report")
    if st.button("Export to CSV"):
        df.to_csv("Abode_Inventory_Report.csv", index=False)
        st.success("Report exported to Abode_Inventory_Report.csv")
    if st.button("Export to Excel"):
        df.to_excel("Abode_Inventory_Report.xlsx", index=False)
        st.success("Report exported to Abode_Inventory_Report.xlsx")

    st.subheader("Charts")
    if not df.empty:
        profit_by_make = df.groupby("Make")["Profit/Loss (₦)"].sum()
        fig1 = plt.figure()
        profit_by_make.plot(kind="bar", color="green")
        plt.title("Total Profit/Loss by Vehicle Make")
        plt.ylabel("Profit/Loss (₦)")
        plt.tight_layout()
        fig1.savefig("profit_by_make.png")
        st.image("profit_by_make.png")

        count_by_make = df["Make"].value_counts()
        fig2 = plt.figure()
        count_by_make.plot(kind="bar", color="blue")
        plt.title("Number of Vehicles by Make")
        plt.ylabel("Count")
        plt.tight_layout()
        fig2.savefig("vehicle_count_by_make.png")
        st.image("vehicle_count_by_make.png")

def staff_dashboard():
    st.subheader("Staff Dashboard")
    df = load_inventory()
    st.dataframe(df)

    st.subheader("Charts")
    if not df.empty:
        st.image("profit_by_make.png")
        st.image("vehicle_count_by_make.png")

if not st.session_state.logged_in:
    login()
else:
    st.sidebar.button("Logout", on_click=logout)
    if st.session_state.role == "admin":
        admin_dashboard()
    elif st.session_state.role == "staff":
        staff_dashboard()
