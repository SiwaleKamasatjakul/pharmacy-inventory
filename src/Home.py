import streamlit as st
import streamlit as st 
import os
import sys
#from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from page.StockAlert import View
from page.Dashboard import DashboardView
from page.DrugRoute import DrugRouteDashbord




# Handle "page" param
query_params = st.query_params
page = query_params.get("page", "home")

# Custom CSS for navbar
st.markdown("""
    <style>
    .navbar {
        background-color: #2ca3fa; 
        padding: 15px;
        border-radius: 8px;
        width: 100%;  
        display: flex;        /* flex layout for links */
        justify-content: center; /* center links horizontally */
    }
    .navbar a {
        color: white !important;
        text-decoration: none;
        margin: 0 15px;
        font-size: 20px;
        font-weight: 500;
    }
    .navbar a:hover {
        color: #ffd700 !important; /* gold hover */
    }
    </style>
""", unsafe_allow_html=True)

# Navbar
st.markdown(f"""
<nav class="navbar">
  <a class="nav-link" href="?page=home">🏠 Home</a>
  <a class="nav-link" href="?page=drug">💊 Drug route tracker</a>
  <a class="nav-link" href="?page=stock">📦 Stock alert</a>
  <a class="nav-link" href="?page=dashboard">📊 Dashboard</a>
</nav>
""", unsafe_allow_html=True)

# Page logic
if page == "home":
    st.title("🏠 Home")
elif page == "drug":
    st.title("💊 Drug route tracker")
    DrugRouteDashbord.dashboard()
    
elif page == "stock":
    
    View.dashbord()
elif page == "dashboard":
    st.title("📊 Dashboard")
    DashboardView.dashboard_view()


