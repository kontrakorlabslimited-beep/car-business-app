
import streamlit as st
import pandas as pd

# Initialize session state for data storage
if 'vehicles' not in st.session_state:
    st.session_state.vehicles = pd.DataFrame(columns=[
        'VIN', 'Make', 'Model', 'Year', 'Purchase Price', 'Import Charges',
        'Other Costs', 'Total Cost', 'Sale Price', 'Repairs', 'Other Expenses',
        'Profit/Loss'
    ])

st.title("🚗 Car Business Management App")

# Sidebar navigation
menu = st.sidebar.radio("Navigate", ["Add Vehicle", "View Inventory", "Profit/Loss Summary"])

if menu == "Add Vehicle":
    st.header("Add Vehicle Transaction")

    with st.form("vehicle_form"):
        vin = st.text_input("VIN")
        make = st.text_input("Make")
        model = st.text_input("Model")
        year = st.number_input("Year", min_value=1900, max_value=2100, step=1)
        purchase_price = st.number_input("Purchase Price", min_value=0.0)
        import_charges = st.number_input("Import Charges", min_value=0.0)
        other_costs = st.number_input("Other Costs", min_value=0.0)
        sale_price = st.number_input("Sale Price", min_value=0.0)
        repairs = st.number_input("Repairs", min_value=0.0)
        other_expenses = st.number_input("Other Expenses", min_value=0.0)

        submitted = st.form_submit_button("Add Vehicle")

        if submitted:
            total_cost = purchase_price + import_charges + other_costs + repairs + other_expenses
            profit_loss = sale_price - total_cost
            new_row = {
                'VIN': vin,
                'Make': make,
                'Model': model,
                'Year': year,
                'Purchase Price': purchase_price,
                'Import Charges': import_charges,
                'Other Costs': other_costs,
                'Total Cost': total_cost,
                'Sale Price': sale_price,
                'Repairs': repairs,
                'Other Expenses': other_expenses,
                'Profit/Loss': profit_loss
            }
            st.session_state.vehicles = pd.concat([st.session_state.vehicles, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Vehicle added successfully!")

elif menu == "View Inventory":
    st.header("Vehicle Inventory")
    st.dataframe(st.session_state.vehicles)

elif menu == "Profit/Loss Summary":
    st.header("Profit/Loss Summary")
    if not st.session_state.vehicles.empty:
        st.dataframe(st.session_state.vehicles[['VIN', 'Make', 'Model', 'Year', 'Total Cost', 'Sale Price', 'Profit/Loss']])
        total_profit = st.session_state.vehicles['Profit/Loss'].sum()
        st.metric("Total Profit/Loss", f"${total_profit:,.2f}")
    else:
        st.info("No data available.")
