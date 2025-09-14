
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load inventory data
inventory_file = "inventory.csv"
if os.path.exists(inventory_file):
    df = pd.read_csv(inventory_file)
else:
    df = pd.DataFrame(columns=[
        "Vehicle ID", "Make", "Model", "Year", "Purchase Price (₦)", "Import Charges (₦)",
        "Repairs (₦)", "Other Expenses (₦)", "Exchange Rate", "Sale Price (₦)",
        "Profit/Loss (₦)", "Profit/Loss ($)", "Status"
    ])

# Calculate profit/loss and status if not already present
if "Profit/Loss (₦)" not in df.columns or df["Profit/Loss (₦)"].isnull().any():
    df["Total Cost (₦)"] = df["Purchase Price (₦)"] + df["Import Charges (₦)"] + df["Repairs (₦)"] + df["Other Expenses (₦)"]
    df["Profit/Loss (₦)"] = df["Sale Price (₦)"] - df["Total Cost (₦)"]
    df["Exchange Rate"] = df.get("Exchange Rate", pd.Series([1000]*len(df)))
    df["Profit/Loss ($)"] = df["Profit/Loss (₦)"] / df["Exchange Rate"]
    df["Status"] = df["Profit/Loss (₦)"].apply(lambda x: "Gain" if x > 0 else ("Loss" if x < 0 else "Break-even"))

# Display inventory summary with full width
st.set_page_config(layout="wide")
st.title("Abode Car Business Management App")
st.subheader("Inventory Summary")

# Apply color coding to Status column
def highlight_status(val):
    color = ''
    if val == 'Gain':
        color = 'background-color: lightgreen'
    elif val == 'Loss':
        color = 'background-color: lightcoral'
    elif val == 'Break-even':
        color = 'background-color: lightgray'
    return color

styled_df = df.style.applymap(highlight_status, subset=["Status"])
st.dataframe(styled_df, use_container_width=True)

# Generate charts
st.subheader("Charts by Vehicle Make")

# Chart 1: Total Profit/Loss by Make
fig1, ax1 = plt.subplots()
profit_by_make = df.groupby("Make")["Profit/Loss (₦)"].sum().sort_values()
sns.barplot(x=profit_by_make.values, y=profit_by_make.index, ax=ax1)
ax1.set_title("Total Profit/Loss by Vehicle Make")
ax1.set_xlabel("Profit/Loss (₦)")
fig1.tight_layout()
fig1.savefig("profit_by_make.png")
st.pyplot(fig1)

# Chart 2: Vehicle Count by Make
fig2, ax2 = plt.subplots()
vehicle_count = df["Make"].value_counts()
sns.barplot(x=vehicle_count.values, y=vehicle_count.index, ax=ax2)
ax2.set_title("Number of Vehicles by Make")
ax2.set_xlabel("Count")
fig2.tight_layout()
fig2.savefig("vehicle_count_by_make.png")
st.pyplot(fig2)

# Save updated inventory
df.to_csv("inventory.csv", index=False)
