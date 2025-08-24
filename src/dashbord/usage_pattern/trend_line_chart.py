import sys
import os
import pandas as pd 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.read_data.read_excel import ReadExcel
import streamlit as st
from datetime import datetime, timedelta
import altair as alt

class TrendLineChart:
    
    @staticmethod
    def trend_line_chart():
        st.title("📈 Trend Data Dashboard")
        
        # Read Excel data
        df = ReadExcel.read_robot_log_excel_convert_to_df()
        
        # Convert datetime column
        df['ข้อมูลเวลา'] = pd.to_datetime(df['ข้อมูลเวลา'])

        # Sidebar: Select shop
        shops = df["ชื่อร้านค้า"].unique().tolist()
        selected_shop = st.selectbox("🏪 Select Shop", shops)

        df_filtered = df[df["ชื่อร้านค้า"] == selected_shop]

        # Sidebar: Choose date filter type
        filter_type = st.radio("📅 Date Filter", ["Today", "Select Date", "Select Week", "Select Month"])

        # Apply date filters
        if filter_type == "Today":
            today = datetime.today().date()
            df_filtered = df_filtered[df_filtered['ข้อมูลเวลา'].dt.date == today]
        elif filter_type == "Select Date":
            selected_date = st.date_input("Select a date", datetime.today())
            df_filtered = df_filtered[df_filtered['ข้อมูลเวลา'].dt.date == selected_date]
        elif filter_type == "Select Week":
            week_start = st.date_input("Week start", datetime.today() - timedelta(days=datetime.today().weekday()))
            week_end = week_start + timedelta(days=6)
            df_filtered = df_filtered[(df_filtered['ข้อมูลเวลา'].dt.date >= week_start) & 
                                      (df_filtered['ข้อมูลเวลา'].dt.date <= week_end)]
        elif filter_type == "Select Month":
            month = st.selectbox("Month", list(range(1, 13)), index=datetime.today().month - 1)
            year = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.today().year)
            df_filtered = df_filtered[(df_filtered['ข้อมูลเวลา'].dt.year == year) & 
                                      (df_filtered['ข้อมูลเวลา'].dt.month == month)]

        if df_filtered.empty:
            st.warning("⚠️ No data for the selected date range.")
            return

        # Aggregate daily jobs
        daily_jobs = (
            df_filtered.groupby(df_filtered['ข้อมูลเวลา'].dt.date)['จำนวนงาน']
            .sum()
            .reset_index()
            .rename(columns={'ข้อมูลเวลา': 'วันที่', 'จำนวนงาน': 'จำนวนงานต่อวัน'})
        )

        # Altair line chart
        line_chart = alt.Chart(daily_jobs).mark_line(point=True).encode(
            x=alt.X('วันที่:T', title='Date'), 
            y=alt.Y('จำนวนงานต่อวัน:Q', title='Jobs per Day'),
            tooltip=['วันที่', 'จำนวนงานต่อวัน']
        ).properties(
            width='container',
            height=400,
            title=f"Daily Jobs Trend for {selected_shop}"
        ).interactive()  # enable zoom/pan

        st.altair_chart(line_chart, use_container_width=True)

        # Optional: show raw data
        with st.expander("Show Raw Data"):
            st.dataframe(daily_jobs)

if __name__ == "__main__":
    TrendLineChart.trend_line_chart()
