import streamlit as st



class View:
    
    @staticmethod
    def dashbord():
import streamlit as st

# Handle "page" param
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["home"])[0]

# Navbar
st.markdown(f"""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #2ca3fa;">
  <a class="nav-link" href="?page=home">Home</a>
  <a class="nav-link" href="?page=drug">Drug route tracker</a>
  <a class="nav-link" href="?page=stock">Stock alert</a>
  <a class="nav-link" href="?page=dashboard">Dashboard</a>
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

if __name__ == "__main__":
    View.dashbord()