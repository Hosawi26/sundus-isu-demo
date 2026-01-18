import streamlit as st
import time
import pandas as pd
from src.logic import TieredLogicEngine, AnomalyEvent
from src.simulation import AnomalyGenerator
from src.sandbox import run_sandbox_test
import io
import sys

# Page Config
st.set_page_config(
    page_title="SUNDUS@ISU Prototype",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Logic
if 'engine' not in st.session_state:
    st.session_state.engine = TieredLogicEngine()
if 'generator' not in st.session_state:
    st.session_state.generator = AnomalyGenerator()
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150?text=SUNDUS@ISU", caption="Human-AI Teaming")
    st.title("Control Panel")
    
    st.markdown("### Simulation Controls")
    if st.button("Inject Random Anomaly"):
        event = st.session_state.generator.generate_event()
        alert = st.session_state.engine.process_anomaly(event)
        st.session_state.history.insert(0, {"time": time.strftime("%H:%M:%S"), "event": event, "alert": alert})
        st.rerun()
        
    st.markdown("### Scenario Playback")
    
    # Get list of IDs
    scenario_ids = [s["id"] for s in st.session_state.generator.scenarios]
    selected_id = st.selectbox("Select Anomaly Clip", scenario_ids)
    
    if st.button("Play Clip"):
        event = st.session_state.generator.get_specific_scenario(selected_id)
        if event:
            alert = st.session_state.engine.process_anomaly(event)
            st.session_state.history.insert(0, {"time": time.strftime("%H:%M:%S"), "event": event, "alert": alert})
            st.rerun()

    st.markdown("---")
    st.markdown("### Diagnostic Tools")
    if st.button("Run Virtual Sandbox Test"):
        # Capture stdout to show in UI
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        try:
            run_sandbox_test()
            result = new_stdout.getvalue()
        except Exception as e:
            result = f"Error running test: {e}"
        finally:
            sys.stdout = old_stdout
            
        st.session_state.sandbox_result = result

# Main Interface
st.title("SUNDUS@ISU: Cognitive Offloading Dashboard")
st.markdown("### Live Anomaly Monitoring Feed")

# Top Status Simulation (Placeholder for Video)
main_col, alert_col = st.columns([2, 1])

with main_col:
    # Check for specific scenario image
    current_event = None
    if st.session_state.history:
        current_event = st.session_state.history[0]['event']
        
    image_path = None
    if current_event:
        # Map IDs to generated images (mock logic or file check)
        # In a real app, these would be mp4 clips
        if current_event.id == "C-02":
             image_path = "assets/c_02_unattended_bag.png" # You will need to move generated artifacts here
        elif current_event.id == "H-03":
             image_path = "assets/h_03_weapon_classroom.png"
        elif current_event.id == "H-04":
             image_path = "assets/h_04_flash_flood.png"
             
    if image_path:
        st.image(image_path, caption=f"LIVE FEED: {current_event.location} [SIMULATION]", use_column_width=True)
    else:
        st.video("https://www.w3schools.com/html/mov_bbb.mp4", format="video/mp4", start_time=0)
        st.caption("Live Camera Feed (Simulated Source via Web)")

with alert_col:
    st.subheader("System Status")
    
    if st.session_state.history:
        latest = st.session_state.history[0]
        alert = latest['alert']
        event = latest['event']
        
        # Dynamic Styling
        color_map = {"green": "success", "orange": "warning", "red": "error"}
        st_func = getattr(st, color_map.get(alert.color, "info"))
        
        st_func(f"**STATUS: {alert.level} - {alert.color.upper()}**")
        
        st.markdown(f"**Detection:** {event.type}")
        st.markdown(f"**Location:** {event.location}")
        
        st.divider()
        st.markdown("#### AI Explanation (NLE)")
        st.info(alert.nle)
        
        if alert.audio_cue:
            st.audio("https://www.soundjay.com/buttons/beep-01a.mp3")
            st.caption("🔊 Audio Cue Triggered")
        
        if alert.strobe:
             st.markdown(":rotating_light: **VISUAL STROBE ACTIVE** :rotating_light:")
    else:
        st.success("System Operational. No anomalies detected.")

# Sandbox Results Area
if 'sandbox_result' in st.session_state:
    st.divider()
    with st.expander("Virtual Sandbox Verify Output", expanded=True):
        st.code(st.session_state.sandbox_result)

# Historical Log
st.divider()
st.subheader("Event Log")
if st.session_state.history:
    data = []
    for item in st.session_state.history:
        data.append({
            "Time": item['time'],
            "Tier": item['alert'].level,
            "Type": item['event'].type,
            "Explanation": item['alert'].nle,
            "Severity": f"{item['event'].severity:.2f}"
        })
    st.dataframe(pd.DataFrame(data))
