import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/data.csv")  # or load Excel
    df['StartTime'] = pd.to_datetime(df['StartTime'])
    return df

df = load_data()

# --- Sidebar Navigation ---
st.sidebar.title("Dashboard Navigation")
page = st.sidebar.radio("Go to", ["Main Dashboard", "Other View"])

# --- Date Range Filter ---
min_date = df['StartTime'].min().date()
max_date = df['StartTime'].max().date()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Filter data
mask = (df['StartTime'].dt.date >= start_date) & (df['StartTime'].dt.date <= end_date)
filtered_df = df.loc[mask]

st.title("📊 Equipment Performance Dashboard")

# --- Metric Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Energy Consumption", f"{filtered_df['Actual_Val'].sum():,.2f} kWh")
with col2:
    st.metric("Avg Temp", f"{filtered_df['Avg_Val'].mean():.2f} °C")
with col3:
    st.metric("Space Utilization", f"{filtered_df['Total_Val'].mean():.2f}%")

# --- Line Chart ---
st.subheader("KPI Trend Over Time")
fig_line = px.line(filtered_df, x="StartTime", y="Actual_Val", color="KPI_Name", title="Actual Values Over Time")
st.plotly_chart(fig_line, use_container_width=True)

# --- Bar Chart (Location-Wise) ---
st.subheader("Metric by Location")
bar_df = filtered_df.groupby("Site")["Actual_Val"].sum().reset_index()
fig_bar = px.bar(bar_df, x="Site", y="Actual_Val", title="Total Actual Value by Site")
st.plotly_chart(fig_bar, use_container_width=True)
