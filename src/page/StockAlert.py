import streamlit as st 
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from calculation.threadhold_inventory import ExpireDateCalculation
from calculation.threadhold_inventory import ReservePharmacyButNoStock

class View:
    
    @staticmethod
    def dashbord():
        # Get Data
        expiredate_df = ExpireDateCalculation.expiredateCalculation()
        reserve_but_no_stock = ReservePharmacyButNoStock.reserved_pharmacy_but_no_stock()
        
        # Page config
        st.set_page_config(page_title="Pharmacy Dashboard", layout="wide")
        
        # Inject Custom CSS
        st.markdown(
            """
            <style>
            .big-title {
                font-size: 40px !important;
                font-weight: bold;
                color: #1f77b4;
                text-align: center;
            }
            .medium-title {
                font-size: 35px !important;
                font-weight: bold;
                color: #ff7f0e;
            }
            .small-title {
                font-size: 30px !important;
                font-weight: normal;
                color: #2ca02c;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Title Section (using the class)
        st.markdown(
            """
            <h1 class="big-title">💊 Pharmacy Stock Monitoring Dashboard</h1>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown("---")

        # Quick Stats Section
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "จำนวนยาที่ใกล้หมดอายุใน 30 วัน",
                f"{len(expiredate_df)} รายการ"
            )
        with col2:
            st.metric(
                "จำนวนยาที่ถูกจองไว้แต่ไม่มี stock",
                f"{len(reserve_but_no_stock)} รายการ"
            )
        
        # Subsection Title Example
        st.markdown('<h2 class="medium-title">📅 รายละเอียดข้อมูล</h2>', unsafe_allow_html=True)

        # Expire Soon Section
        with st.expander("🔴 รายการยาที่ใกล้หมดอายุในอีก 30 วัน", expanded=True):
            st.dataframe(expiredate_df, use_container_width=True)

        # Reserved but No Stock Section
        with st.expander("⚠️ รายการยาที่ถูกจองไว้แต่ไม่มี stock ยาเหลือ", expanded=True):
            st.dataframe(reserve_but_no_stock, use_container_width=True)
        

if __name__ == "__main__":
    View.dashbord()
