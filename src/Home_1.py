import streamlit as st


# Handle "page" param
query_params = st.query_params
page = query_params.get("page", "home")

# Custom CSS for navbar
st.markdown("""
    <style>
    .navbar {
        background-color: #2ca3fa; 
        padding: 25px 50px;   /* more vertical and horizontal padding */
        border-radius: 8px;
        width: 100%;          /* full width */
        display: flex;        /* flex layout for links */
        justify-content: center; /* center links horizontally */
        box-sizing: border-box;  /* include padding in width */
    }
    .navbar a {
        color: white !important;
        text-decoration: none;
        margin: 0 25px;
        font-size: 25px;
        font-weight: 500;
        transition: all 0.3s ease;
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
elif page == "stock":
    st.title("📦 Stock alert")
elif page == "dashboard":
    st.title("📊 Dashboard")

