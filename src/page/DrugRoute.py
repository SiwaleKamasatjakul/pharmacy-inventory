import streamlit as st
from datetime import datetime

import streamlit as st
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

import time


class DrugRouteDashbord:

    @staticmethod
    def dashboard():
        st.set_page_config(page_title="💊 Drug route tracker", layout="wide")
        st.markdown("---")

        # Initialize session state
        if "page" not in st.session_state:
            st.session_state.page = "home"

        # ---------------- HOME PAGE ----------------
        if st.session_state.page == "home":
           
            col1, col2, col3 = st.columns([1, 2, 1])

            # Centered content in middle column
            with col2:
                # Date & Time Input
                st.title("🏠 Home")
                datetime_data = datetime.now()
                st.write(f"**DateTime:** {datetime_data.strftime('%Y-%m-%d %H:%M:%S')}")

                # Buttons
                if st.button("🚨 Emergency", key="home_emergency"):
                    st.session_state.page = "emergency"
                    st.rerun()
                if st.button("✅ Normal", key="home_normal"):
                    st.session_state.page = "in_transit"
                    st.rerun()

        # ---------------- EMERGENCY PAGE ----------------
        elif st.session_state.page == "emergency":
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.title("🚨 Emergency Page: Wait for Pack")

                # Date & Time Input
                emergency_time = datetime.now()
                st.write(f"**DateTime:** {emergency_time.strftime('%Y-%m-%d %H:%M:%S')}")



                # Buttons
                if st.button("📦 Finish Pack", key="em_finish"):
                    st.success(f"Packing finished at {emergency_time}!")
                    st.session_state.page = "in_transit"
                    st.rerun()
                
                                    # Signature box
                st.subheader("Receiver Signature")
                canvas_result = st_canvas(
                    fill_color="rgba(0, 0, 0, 0)",
                    stroke_width=3,
                    stroke_color="black",
                    background_color="white",
                    height=200,
                    width=400,
                    key="signature_canvas"
                )

                # Optional: save signature
                if canvas_result.image_data is not None:
                    st.image(canvas_result.image_data, caption="Your Signature")


                # Back button
                if st.button("⬅️ Back to Home", key="em_back"):
                    st.session_state.page = "home"
                    st.rerun()

        # ---------------- IN TRANSIT PAGE ----------------
        elif st.session_state.page == "in_transit":
            # Center progress/metrics in middle column
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.title("🚚 In Transit")
                st.write("Tracking progress...")
                st.progress(50)
                st.metric(label="Estimated Arrival (mins)", value=25)
                st.success("Package is on the way 🚀")

            # Center iPhone UI + back button in middle column
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("""
                <div style="
                    width:375px;
                    height:812px;
                    border:2px solid #ccc;
                    border-radius:40px;
                    box-shadow:0px 8px 20px rgba(0,0,0,0.25);
                    background-color:white;
                    padding:25px;
                    text-align:center;
                    overflow:hidden;
                    margin-top:20px;
                ">
                    <h2 style="color:#333; margin-bottom:20px;">🍏 Apple Box</h2>
                    <p style="font-size:16px; line-height:1.5;">
                        This is an example app interface styled like an iPhone 11 screen.
                    </p>

                    <button style="
                        background-color:#007aff;
                        color:white;
                        padding:12px 24px;
                        font-size:16px;
                        border:none;
                        border-radius:12px;
                        cursor:pointer;
                        margin-top:30px;">
                        Open App
                    </button>
                </div>
                """, unsafe_allow_html=True)

                # Back button centered below iPhone UI
                if st.button("⬅️ Back to Home", key="in_back_transit"):
                    st.session_state.page = "home"
                    st.rerun()
                    
                                # Wait 5 seconds then go to delivery
                if "transit_done" not in st.session_state:
                    time.sleep(5)
                    st.session_state.page = "delivery"
                    st.session_state.transit_done = True
                    st.rerun()
                # ---------------- DELIVERY PAGE ----------------
        elif st.session_state.page == "delivery":
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.title("📦 Delivery Page")
                delivery_time = datetime.now()
                st.write(f"**Delivery Time:** {delivery_time.strftime('%Y-%m-%d %H:%M:%S')}")

                # Receive button
                if st.button("1. Receive Package", key="receive_button"):
                    st.success("Package received!")

                # Signature box
                st.subheader("Receiver Signature")
                canvas_result = st_canvas(
                    fill_color="rgba(0, 0, 0, 0)",
                    stroke_width=3,
                    stroke_color="black",
                    background_color="white",
                    height=200,
                    width=400,
                    key="signature_canvas"
                )

                # Optional: save signature
                if canvas_result.image_data is not None:
                    st.image(canvas_result.image_data, caption="Receiver Signature Saved ✅")