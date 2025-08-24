import streamlit as st 
import os
import sys
#from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))



from src.calculation.threadhold_inventory import ExpireDateCalculation
from src.calculation.threadhold_inventory import ReservePharmacyButNoStock

class View:
    
    @staticmethod
    def dashbord():
        
        
        expiredate_df = ExpireDateCalculation.expiredateCalculation()
        reserve_but_no_stock = ReservePharmacyButNoStock.reserved_pharmacy_but_no_stock()
        
        
        st.header("ตรวจสอบ stock ยา")
        st.title("รายการยาที่ใกล้หมดอายุในอีก 30 วัน")
        st.dataframe(expiredate_df)

        st.title("รายการยาที่มีการจองไว้แต่ไม่มี stock ยาเหลือไว้")
        st.dataframe(reserve_but_no_stock)
        
        
if __name__ == "__main__":
    View.dashbord()