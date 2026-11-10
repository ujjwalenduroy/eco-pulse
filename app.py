import streamlit as st
import pickle
import os

st.set_page_config(page_title="EcoPulse - Smart Campus Energy Optimizer", page_icon="⚡", layout="centered")

# Load model weights
if os.path.exists('model.pkl'):
    with open('model.pkl', 'rb') as f:
        weights = pickle.load(f)
else:
    weights = {'w_temp': 0.05, 'w_occ': 1.50, 'w_hours': 0.45, 'bias': -1.2}

st.title("⚡ EcoPulse Dashboard")
st.write("AI-Driven Campus Power Wastage & Load Predictor")

st.markdown("---")

# Input controls
temp = st.slider("Ambient Temperature (°C)", 15, 50, 30)
occupancy_choice = st.selectbox("Room Occupancy Status", ["Occupied (1)", "Vacant (0)"])
occupancy = 1 if "1" in occupancy_choice else 0
hours = st.number_input("Active Hours Today", min_value=1.0, max_value=24.0, value=5.0)

if st.button("Run AI Analysis", type="primary"):
    prediction = (temp * weights['w_temp']) + (occupancy * weights['w_occ']) + (hours * weights['w_hours']) + weights['bias']
    prediction = max(0.1, prediction)
    
    status = "Normal"
    if occupancy == 0 and hours > 2:
        status = "Wastage Alert: Appliance running in an empty room!"
    elif prediction > 5.0:
        status = "High Load Warning: Consuming high power."

    st.markdown("### Prediction Results")
    st.metric(label="Predicted Energy Consumption", value=f"{round(prediction, 2)} kWh")
    
    if "Alert" in status or "Warning" in status:
        st.error(f"System Status: {status}")
    else:
        st.success(f"System Status: {status}")