import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.read_data.read_excel import ReadExcel
import streamlit as st
from datetime import datetime, timedelta

class ProductivityDF:

    @staticmethod
    def productivity_dataframe():

        # Page title
        st.title("📊 Productivity Dashboard")
        st.markdown("---")

        # Read Excel data
        df = ReadExcel.read_robot_log_excel_convert_to_df()
        df['ข้อมูลเวลา'] = pd.to_datetime(df['ข้อมูลเวลา'])

        # Compute productivity metrics
        df["job_per_hour"] = df["จำนวนงาน"] / df["ระยะเวลาการทำงาน (h)"]
        df["job_per_distance"] = df["จำนวนงาน"] / df["ระยะทางการทำงาน (km)"]

        # Shop selection
        shops = df["ชื่อร้านค้า"].unique().tolist()
        selected_shop = st.selectbox("🏪 Select Shop", shops, key="productivity_shop_select")

        # Filter by shop
        df_filtered = df[df["ชื่อร้านค้า"] == selected_shop]

        # Date filter
        filter_type = st.radio(
            "📅 Date Filter",
            ["Today", "Select Date", "Select Week", "Select Month"],
            key="productivity_filter_type"
        )

        # Apply date filters
        if filter_type == "Today":
            today = datetime.today().date()
            df_filtered = df_filtered[df_filtered['ข้อมูลเวลา'].dt.date == today]
        elif filter_type == "Select Date":
            selected_date = st.date_input("Select a date", datetime.today(), key="productivity_date_input")
            df_filtered = df_filtered[df_filtered['ข้อมูลเวลา'].dt.date == selected_date]
        elif filter_type == "Select Week":
            week_start = st.date_input("Week start", datetime.today() - timedelta(days=datetime.today().weekday()), key="productivity_week_start")
            week_end = week_start + timedelta(days=6)
            df_filtered = df_filtered[(df_filtered['ข้อมูลเวลา'].dt.date >= week_start) &
                                      (df_filtered['ข้อมูลเวลา'].dt.date <= week_end)]
        elif filter_type == "Select Month":
            month = st.selectbox("Month", list(range(1, 13)), index=datetime.today().month-1, key="productivity_month_select")
            year = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.today().year, key="productivity_year_select")
            df_filtered = df_filtered[(df_filtered['ข้อมูลเวลา'].dt.year == year) &
                                      (df_filtered['ข้อมูลเวลา'].dt.month == month)]

        # Handle empty data
        if df_filtered.empty:
            st.warning("⚠️ No data for the selected date range.")
            return

        # Aggregate metrics
        df_job_per_hour = (
            df_filtered.groupby(df_filtered['ข้อมูลเวลา'].dt.date)['job_per_hour']
            .sum().reset_index()
            .rename(columns={'ข้อมูลเวลา': 'วันที่', 'job_per_hour': 'งาน/ระยะเวลาการทำงาน'})
        )
        df_job_per_distance = (
            df_filtered.groupby(df_filtered['ข้อมูลเวลา'].dt.date)['job_per_distance']
            .sum().reset_index()
            .rename(columns={'ข้อมูลเวลา': 'วันที่', 'job_per_distance': 'งาน/ระยะทางการทำงาน'})
        )

        # Add shop name
        df_job_per_hour['ชื่อร้านค้า'] = selected_shop
        df_job_per_distance['ชื่อร้านค้า'] = selected_shop

        '''
        # Display metrics summary
        total_jobs = df_filtered["จำนวนงาน"].sum()
        total_distance = df_filtered["ระยะทางการทำงาน (km)"].sum()
        total_hours = df_filtered["ระยะเวลาการทำงาน (h)"].sum()
        avg_job_per_hour = round(df_filtered["job_per_hour"].mean(), 2)
        avg_job_per_distance = round(df_filtered["job_per_distance"].mean(), 2)

        st.markdown("### 📌 Summary Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Jobs", total_jobs)
        col2.metric("Total Hours", total_hours)
        col3.metric("Total Distance (km)", total_distance)

        col4, col5 = st.columns(2)
        col4.metric("Avg Jobs/Hour", avg_job_per_hour)
        col5.metric("Avg Jobs/Distance", avg_job_per_distance)
        '''
        st.markdown("---")

        # Display aggregated dataframes
        st.subheader("Job per Hour (Aggregated by Date)")
        st.dataframe(df_job_per_hour[["วันที่", "ชื่อร้านค้า", "งาน/ระยะเวลาการทำงาน"]], use_container_width=True)

        st.subheader("Job per Distance (Aggregated by Date)")
        st.dataframe(df_job_per_distance[["วันที่", "ชื่อร้านค้า", "งาน/ระยะทางการทำงาน"]], use_container_width=True)
