import sys
import os
import pandas as pd 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.read_data.read_excel import ReadExcel
import streamlit as st
from datetime import datetime, timedelta
import altair as alt

class EfficiencyLineChart:

    @staticmethod
    def efficiency_line_chart():
        # Page layout: wide for flexibility
        st.set_page_config(
            page_title="Robot Efficiency Dashboard",
            page_icon="🤖",
            layout="wide"
        )

        st.title("🤖 Robot Efficiency Dashboard")
        st.markdown("---")

        # Read data
        df = ReadExcel.read_robot_log_excel_convert_to_df()
        df['ข้อมูลเวลา'] = pd.to_datetime(df['ข้อมูลเวลา'])
        df["efficiency"] = df["จำนวนปลายทาง"] / df["ระยะทางการทำงาน (km)"]

        # Sidebar filters
        shops = df["ชื่อร้านค้า"].unique().tolist()
        selected_shop = st.selectbox("🏪 Select Shop", shops, key="efficiency_shop_select")
        filter_type = st.radio(
            "📅 Date Filter", 
            ["Today", "Select Date", "Select Week", "Select Month"], 
            key="efficiency_date_filter"
        )

        # Filter by shop
        df_filtered = df[df["ชื่อร้านค้า"] == selected_shop]

        # Date filtering
        if filter_type == "Today":
            today = datetime.today().date()
            df_filtered = df_filtered[df_filtered['ข้อมูลเวลา'].dt.date == today]
        elif filter_type == "Select Date":
            selected_date = st.date_input("Select a date", datetime.today(), key="efficiency_date_input")
            df_filtered = df_filtered[df_filtered['ข้อมูลเวลา'].dt.date == selected_date]
        elif filter_type == "Select Week":
            week_start = st.date_input("Week start", datetime.today() - timedelta(days=datetime.today().weekday()), key="efficiency_week_start")
            week_end = week_start + timedelta(days=6)
            df_filtered = df_filtered[(df_filtered['ข้อมูลเวลา'].dt.date >= week_start) & (df_filtered['ข้อมูลเวลา'].dt.date <= week_end)]
        elif filter_type == "Select Month":
            month = st.selectbox("Month", list(range(1,13)), index=datetime.today().month-1, key="efficiency_month_select")
            year = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.today().year, key="efficiency_year_select")
            df_filtered = df_filtered[(df_filtered['ข้อมูลเวลา'].dt.year == year) & (df_filtered['ข้อมูลเวลา'].dt.month == month)]

        if df_filtered.empty:
            st.warning("⚠️ No data for the selected date range.")
            return

        # Metrics summary in medium-width columns
        col1, col2, col3 = st.columns([1,1,1])  # 3 equal-width columns
        col1.metric("Total Jobs", df_filtered["จำนวนปลายทาง"].sum())
        col2.metric("Total Distance (km)", df_filtered["ระยะทางการทำงาน (km)"].sum())
        #col3.metric("Average Efficiency", round(df_filtered["efficiency"].mean(), 2))

        st.markdown("### 📈 Efficiency Over Time")

        # Pivot the data
        pivot_df = df_filtered.pivot_table(
            values="efficiency",
            index="ข้อมูลเวลา",
            columns="ชื่อร้านค้า"
        ).reset_index()

        # Melt DataFrame to long format for Altair
        df_long = pivot_df.melt(id_vars='ข้อมูลเวลา', var_name='Shop', value_name='Efficiency')

        # Altair line chart
        line_chart = alt.Chart(df_long).mark_line(point=True).encode(
            x=alt.X('ข้อมูลเวลา:T', title='Date'),           # X-axis title
            y=alt.Y('Efficiency:Q', title='Efficiency'),   # Y-axis title
            color='Shop:N',                                 # Lines by shop
            tooltip=['ข้อมูลเวลา', 'Shop', 'Efficiency']    # Tooltip info
        ).properties(
            width='container',  # fill container width
            height=400,
            title="📈 Robot Efficiency Over Time"  # Chart title
        ).interactive()  # allow zoom and pan

        st.altair_chart(line_chart, use_container_width=True)

        # Optional: raw data in medium width
        with st.expander("Show Raw Data"):
            st.dataframe(df_filtered)
        st.markdown("---")

if __name__ == "__main__":
    EfficiencyLineChart.efficiency_line_chart()
