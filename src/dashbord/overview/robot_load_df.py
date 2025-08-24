import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.read_data.read_excel import ReadExcel
import streamlit as st
from datetime import datetime, timedelta

class RobotLoadDF:

    @staticmethod
    def robot_load_dataframe():

        # Set Streamlit wide layout
        st.set_page_config(
            page_title="Robot Load Dashboard",
            page_icon="🤖",
            layout="wide"
        )

        # Custom CSS for font size
        st.markdown("""
            <style>
            .title {
                font-size: 36px !important;
                font-weight: bold;
                color: #1f77b4;
                text-align: center;
            }
            .metric-value {
                font-size: 22px !important;
                font-weight: bold;
            }
            .metric-label {
                font-size: 18px !important;
                font-weight: normal;
            }
            </style>
        """, unsafe_allow_html=True)

        # Page title

        st.title("🤖 Robot Load Dashboard")
        st.markdown("---")

        # Read Excel data
        df = ReadExcel.read_robot_log_excel_convert_to_df()
        df['ข้อมูลเวลา'] = pd.to_datetime(df['ข้อมูลเวลา'])

        # Compute robot load
        df["robot_load"] = df["จำนวนงาน"] / df["จำนวนถาด"]

        # Shop selection
        shops = df["ชื่อร้านค้า"].unique().tolist()
        selected_shop = st.selectbox("🏪 Select Shop", shops, key="robot_load_shop_select")

        # Filter by shop
        df_filtered = df[df["ชื่อร้านค้า"] == selected_shop]

        # Date filter
        filter_type = st.radio(
            "📅 Date Filter",
            ["Today", "Select Date", "Select Week", "Select Month"],
            key="robot_load_date_filter",
            horizontal=True
        )

        # Apply date filter
        if filter_type == "Today":
            today = datetime.today().date()
            df_filtered = df_filtered[df_filtered['ข้อมูลเวลา'].dt.date == today]

        elif filter_type == "Select Date":
            selected_date = st.date_input("Select a date", datetime.today(), key="robot_load_date_input")
            df_filtered = df_filtered[df_filtered['ข้อมูลเวลา'].dt.date == selected_date]

        elif filter_type == "Select Week":
            week_start = st.date_input("Week start", datetime.today() - timedelta(days=datetime.today().weekday()), key="robot_load_week_start")
            week_end = week_start + timedelta(days=6)
            df_filtered = df_filtered[(df_filtered['ข้อมูลเวลา'].dt.date >= week_start) & 
                                      (df_filtered['ข้อมูลเวลา'].dt.date <= week_end)]

        elif filter_type == "Select Month":
            month = st.selectbox("Month", list(range(1, 13)), index=datetime.today().month-1, key="robot_load_month_select")
            year = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.today().year, key="robot_load_year_select")
            df_filtered = df_filtered[(df_filtered['ข้อมูลเวลา'].dt.year == year) &
                                      (df_filtered['ข้อมูลเวลา'].dt.month == month)]

        if df_filtered.empty:
            st.warning("⚠️ No data for the selected date range.")
            return

        # Aggregate robot load by date
        df_summary = df_filtered.copy()
        df_summary['วันที่'] = df_summary['ข้อมูลเวลา'].dt.date  # create date column
        df_summary = df_summary.groupby('วันที่', as_index=False)['robot_load'].sum()
        df_summary.rename(columns={'robot_load': 'Robot Load'}, inplace=True)
        df_summary['Shop'] = selected_shop

        # Display metrics summary
        total_jobs = df_filtered["จำนวนงาน"].sum()
        total_trays = df_filtered["จำนวนถาด"].sum()
        #avg_load = round(df_filtered["robot_load"].mean(), 2)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Jobs", total_jobs)
        col2.metric("Total Trays", total_trays)
        #col3.metric("Average Load", avg_load)

        st.markdown("### 📊 Robot Load by Date")
        st.dataframe(df_summary[["วันที่", "Shop", "Robot Load"]], use_container_width=True)
        st.markdown("---")

# Streamlit main
if __name__ == "__main__":
    RobotLoadDF.robot_load_dataframe()
