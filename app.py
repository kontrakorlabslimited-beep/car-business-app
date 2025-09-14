
import streamlit as st
import pandas as pd
import os
from PIL import Image
import plotly.express as px

st.set_page_config(layout="wide")
if os.path.exists("abode_logo.png"):
    st.image("abode_logo.png", width=150)

st.title("Abode Car Business Management App")

inventory_file = "inventory.csv"
if os.path.exists(inventory_file):
    df = pd.read_csv(inventory_file)
else:
    st.warning("No inventory data found.")
    st.stop()

df["Total Cost (₦)"] = df[["Purchase Price (₦)", "Import Charges (₦)", "Other Expenses (₦)", "Repairs (₦)"]].sum(axis=1)
df["Profit/Loss (₦)"] = df["Sale Price (₦)"] - df["Total Cost (₦)"]
df["Profit/Loss ($)"] = df["Profit/Loss (₦)"] / df["Exchange Rate"]
df["Status"] = df["Profit/Loss (₦)"].apply(lambda x: "Gain" if x > 0 else ("Loss" if x < 0 else "Break-even"))

st.subheader("Inventory Summary")
def highlight_status(val):
    color = 'green' if val == "Gain" else ('red' if val == "Loss" else 'gray')
    return f'background-color: {color}; color: white'

st.dataframe(df.style.applymap(highlight_status, subset=["Status"]), use_container_width=True)

st.subheader("Charts")
if os.path.exists("profit_by_make_chart.png"):
    st.image("profit_by_make_chart.png", caption="Total Profit/Loss by Vehicle Make")
if os.path.exists("count_by_make_chart.png"):
    st.image("count_by_make_chart.png", caption="Number of Vehicles by Make")
