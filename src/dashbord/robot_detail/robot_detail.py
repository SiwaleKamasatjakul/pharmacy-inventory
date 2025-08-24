

import sys
import os
import pandas as pd 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#from load_config.loader_config import GetSetting
from src.read_data.read_excel import ReadExcel
import streamlit as st
from datetime import datetime, timedelta


class RobotDetail:
    
    @staticmethod
    def robot_detail():
        st.title("Robot Detail")
        df = ReadExcel.read_robot_log_excel_convert_to_df()
        print(df.head(5))
        print(df.info())

        # Convert datetime column
        df['ข้อมูลเวลา'] = pd.to_datetime(df['ข้อมูลเวลา'])

        # Sidebar: Select shop
        shops = df["ชื่อร้านค้า"].unique().tolist()
        robot_id = df["SN (PID)"].unique().tolist()
        selected_shop = st.selectbox("ร้านค้า", shops)
        selected_robot_id = st.selectbox("สินค้า",robot_id)

        df_filtered = df[df["ชื่อร้านค้า"] == selected_shop]
        df_filtered = df[df["SN (PID)"] == selected_robot_id]
        
        # Sidebar: Choose date filter type
        filter_type = st.radio("Date filter", ["Today", "Select Date", "Select Week", "Select Month"])

        if filter_type == "Today":
            today = datetime.today().date()
            df_filtered = df_filtered[df_filtered['ข้อมูลเวลา'].dt.date == today]
        elif filter_type == "Select Date":
            selected_date = st.date_input("Select a date", datetime.today())
            df_filtered = df_filtered[df_filtered['ข้อมูลเวลา'].dt.date == selected_date]
        elif filter_type == "Select Week":
            week_start = st.date_input("Week start", datetime.today() - timedelta(days=datetime.today().weekday()))
            week_end = week_start + timedelta(days=6)
            df_filtered = df_filtered[(df_filtered['ข้อมูลเวลา'].dt.date >= week_start) & (df_filtered['ข้อมูลเวลา'].dt.date <= week_end)]
        elif filter_type == "Select Month":
            month = st.selectbox("Month", list(range(1, 13)), index=datetime.today().month - 1)
            year = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.today().year)
            df_filtered = df_filtered[(df_filtered['ข้อมูลเวลา'].dt.year == year) & (df_filtered['ข้อมูลเวลา'].dt.month == month)]

        if df_filtered.empty:
            st.warning("No data for the selected date range.")
            return

        grouped = df_filtered.groupby(['SN (PID)']).agg({
            
            'ระยะเวลาการทำงาน (h)': 'sum',
            'ระยะทางการทำงาน (km)': 'sum',
            'ความเร็วการทำงานเฉลี่ย (m/s)': 'sum',
            'จำนวนปลายทาง': 'sum',
            'จำนวนถาด': 'sum'
            
        }).reset_index()
        
                # Optional: Show raw grouped data
        st.title("Show robot detail data")
        st.dataframe(grouped)



if __name__ == "__main__":
    RobotDetail.robot_detail()
