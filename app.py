import streamlit as st
import json
import time
import os

# Page Config
st.set_page_config(
    page_title="SUNDUS@ISU Prototype",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Anomalies
@st.cache_data
def load_anomalies():
    file_path = 'anomalies.json'
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return json.load(f)

anomalies = load_anomalies()

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150?text=SUNDUS@ISU", caption="Human-AI Teaming")
    st.title("Control Panel")
    
    st.markdown("### Anomaly Selection")
    
    if anomalies:
        # Create options [ID]: [Name]
        options = [f"{a['id']}: {a['name']}" for a in anomalies]
        selected_option = st.selectbox("Select Anomaly Scenario", options)
        
        # Find selected anomaly data
        selected_id = selected_option.split(":")[0]
        selected_anomaly = next((a for a in anomalies if a['id'] == selected_id), None)
        
        run_test = st.button("Run System Test", type="primary")
    else:
        st.error("anomalies.json not found or empty.")
        selected_anomaly = None
        run_test = False

# Main Interface
st.title("SUNDUS@ISU: System for Understanding, Navigating, and Decision-Making Under Uncertainty and Support")

# Initialize session state for "active test"
if 'active_test' not in st.session_state:
    st.session_state.active_test = None

if run_test and selected_anomaly:
    with st.spinner("Initializing AI Neural Transparency Layer..."):
        time.sleep(2) # Simulate AI thinking
    st.session_state.active_test = selected_anomaly
    st.rerun()

# Display Logic
if st.session_state.active_test:
    anomaly = st.session_state.active_test
    
    # Multisensory Trigger
    is_high_severity = anomaly.get('multisensory', False) or anomaly['id'].startswith('H')
    
    if is_high_severity:
        # Flash Red Theme Simulation (using experimental st.markdown to inject CSS)
        st.markdown(
            """
            <style>
            .stAppViewContainer {
                background-color: #2b0000;
            }
            .stMain {
                background-color: #2b0000;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.error(f"⚠️ HIGH SEVERITY ALERT: {anomaly['name']} ⚠️")
        
        # Audio Alert
        st.audio("https://www.soundjay.com/buttons/beep-01a.mp3", autoplay=True)
    else:
         # Reset background (attempt to reset)
         st.markdown(
            """
            <style>
            .stAppViewContainer {
                background-color: #0e1117; 
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    col_video, col_info = st.columns([1.5, 1])
    
    with col_video:
        st.subheader(f"Video Feed Ref: {anomaly['id']}")
        video_path = f"assets/{anomaly['video_file']}"
        
        if os.path.exists(video_path):
             st.video(video_path, autoplay=True)
        else:
             st.warning(f"Video file source not found: {video_path}")
             # Fallback
             st.video("https://www.w3schools.com/html/mov_bbb.mp4")

    with col_info:
        st.subheader("AI Decision Logic (Transparency Layer)")
        
        # Metrics
        m1, m2 = st.columns(2)
        m1.metric("Severity", anomaly['severity'])
        m2.metric("Confidence", anomaly['confidence'])
        
        st.divider()
        
        st.markdown("#### 🧠 Natural Language Explanation (NLE)")
        st.info(anomaly['nle'])
        
        st.markdown("#### 🛡️ Suggested Corrective Action (SCA)")
        st.success(anomaly['sca'])

else:
    st.info("System Ready. Select an anomaly from the sidebar and click 'Run System Test'.")
