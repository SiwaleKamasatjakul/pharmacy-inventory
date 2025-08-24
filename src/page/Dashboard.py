import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dashbord.overview.efficiency_line_chart import EfficiencyLineChart
from dashbord.usage_pattern.trend_line_chart import TrendLineChart
from dashbord.usage_pattern.heatmap_job import HeatmapJob
from dashbord.robot_detail.robot_detail import RobotDetail
from dashbord.overview.robot_load_df import RobotLoadDF
from dashbord.overview.productivity import ProductivityDF
import streamlit as st
from src.dashbord.overview.efficiency_line_chart import EfficiencyLineChart
from src.dashbord.overview.robot_load_df import RobotLoadDF
from src.dashbord.overview.productivity import ProductivityDF
from src.dashbord.usage_pattern.trend_line_chart import TrendLineChart
from src.dashbord.usage_pattern.heatmap_job import HeatmapJob
from src.dashbord.robot_detail.robot_detail import RobotDetail

class DashboardView:

    @staticmethod
    def dashboard_view():

        # Page title
        st.set_page_config(
            page_title="Robot Dashboard",
            page_icon="🤖",
            layout="wide"
        )



        # Buttons for page selection (centered)
        cols = st.columns([1, 2, 2, 2, 1])  # empty columns on sides for centering
        button_style = "width:100%; padding:0.5rem; font-size:1rem; background-color:#1f77b4; color:white; border-radius:5px;"

        with cols[1]:
            if st.button("Overview", key="btn_overview"):
                st.session_state['page'] = "overview"
        with cols[2]:
            if st.button("Usage Pattern", key="btn_usage_pattern"):
                st.session_state['page'] = "usage_pattern"
        with cols[3]:
            if st.button("Robot Detail", key="btn_robot_detail"):
                st.session_state['page'] = "robot_detail"

        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing

        # Default page
        if 'page' not in st.session_state:
            st.session_state['page'] = "overview"

        # Page logic
        page = st.session_state['page']

        if page == "overview":
            st.markdown("<h1 style='text-align:center; color:#ff7f0e; font-size:48px;'>🏠 Overview</h1>", unsafe_allow_html=True)
            st.markdown("---")
            EfficiencyLineChart.efficiency_line_chart()
            RobotLoadDF.robot_load_dataframe()
            ProductivityDF.productivity_dataframe()

        elif page == "usage_pattern":
            st.markdown("<h1 style='text-align:center; color:#2ca02c; font-size:48px;'>💊 Usage Pattern</h1>", unsafe_allow_html=True)
            st.markdown("---")
            TrendLineChart.trend_line_chart()
            HeatmapJob.heatmap_job()

        elif page == "robot_detail":
            st.markdown("<h1 style='text-align:center; color:#d62728; font-size:48px;'>📦 Robot Detail</h1>", unsafe_allow_html=True)
            st.markdown("---")
            RobotDetail.robot_detail()
