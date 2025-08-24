import sys
import os
import pandas as pd 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#from load_config.loader_config import GetSetting
from src.read_data.read_excel import ReadExcel
import streamlit as st
from datetime import datetime, timedelta


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class HeatmapJob:
    
    @staticmethod
    def heatmap_job():
        st.title("📊 Heatmap Job (Jobs per Hour/Day)")

        df = ReadExcel.read_robot_log_excel_convert_to_df()

        # Convert datetime column
        df['ข้อมูลเวลา'] = pd.to_datetime(df['ข้อมูลเวลา'])

        # Sidebar: Select shop
        # Sidebar: Select shop
        shops = df["ชื่อร้านค้า"].unique().tolist()
        selected_shop = st.selectbox("ร้านค้า", shops, key="heatmap_shop_selector")
        df_filtered = df[df["ชื่อร้านค้า"] == selected_shop]
        # Sidebar: Choose date filter type
        filter_type = st.radio(
            "Date filter", 
            ["Today", "Select Date", "Select Week", "Select Month"], 
            key="heatmap_date_filter"
        )

        if filter_type == "Today":
            today = datetime.today().date()
            df_filtered = df_filtered[df_filtered['ข้อมูลเวลา'].dt.date == today]
        elif filter_type == "Select Date":
            selected_date = st.date_input("Select a date", datetime.today(), key="heatmap_date_input")
            df_filtered = df_filtered[df_filtered['ข้อมูลเวลา'].dt.date == selected_date]
        elif filter_type == "Select Week":
            week_start = st.date_input("Week start", datetime.today() - timedelta(days=datetime.today().weekday()), key="heatmap_week_start")
            week_end = week_start + timedelta(days=6)
            df_filtered = df_filtered[(df_filtered['ข้อมูลเวลา'].dt.date >= week_start) & (df_filtered['ข้อมูลเวลา'].dt.date <= week_end)]
        elif filter_type == "Select Month":
            month = st.selectbox("Month", list(range(1, 13)), index=datetime.today().month - 1, key="heatmap_month")
            year = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.today().year, key="heatmap_year")
            df_filtered = df_filtered[(df_filtered['ข้อมูลเวลา'].dt.year == year) & (df_filtered['ข้อมูลเวลา'].dt.month == month)]

        if df_filtered.empty:
            st.warning("⚠️ No data for the selected date range.")
            return

        # Extract hour and date
        df_filtered['Hour'] = df_filtered['ข้อมูลเวลา'].dt.hour
        df_filtered['Date'] = df_filtered['ข้อมูลเวลา'].dt.date

        # Group by Date and Hour → sum จำนวนงาน
        heatmap_data = (
            df_filtered.groupby(['Date', 'Hour'])['จำนวนงาน']
            .sum()
            .reset_index()
        )

        # Pivot for heatmap (rows=Date, cols=Hour)
        heatmap_pivot = heatmap_data.pivot(index="Date", columns="Hour", values="จำนวนงาน").fillna(0)

        # Plot heatmap
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(heatmap_pivot, cmap="YlOrRd", annot=True, fmt=".0f", linewidths=0.5, ax=ax)
        plt.title(f"Heatmap for {selected_shop}", fontsize=14)

        st.pyplot(fig)

        # Optional: Show raw grouped data
        with st.expander("Show raw heatmap data"):
            st.dataframe(heatmap_data)


if __name__ == "__main__":
    HeatmapJob.heatmap_job()
