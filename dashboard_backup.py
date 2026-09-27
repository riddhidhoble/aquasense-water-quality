import streamlit as st
import requests

st.set_page_config(
    page_title="Smart Water Quality Monitoring",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Smart Water Quality Monitoring System")
st.write("AI-Based Water Quality Detection")

st.subheader("Enter Water Parameters")

col1, col2 = st.columns(2)

with col1:
    ph = st.number_input(
        "pH",
        min_value=0.0,
        max_value=14.0,
        value=7.0
    )

    tds = st.number_input(
        "TDS (ppm)",
        min_value=0.0,
        value=100.0
    )

with col2:
    turbidity = st.number_input(
        "Turbidity (NTU)",
        min_value=0.0,
        value=1.0
    )

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        value=25.0
    )

if st.button("Check Water Quality"):

    data = {
        "pH": ph,
        "TDS_ppm": tds,
        "Turbidity_NTU": turbidity,
        "Temperature_C": temperature
    }

    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json=data
        )

        result = response.json()

        if response.status_code == 200:

            prediction = result["prediction"]

            st.subheader("Water Quality Result")

            if prediction.lower() == "safe":
                st.success("✅ WATER IS SAFE")

            else:
                st.error("⚠️ WATER IS UNSAFE")

        else:
            st.error(f"Prediction error: {result.get('error', 'Unknown error')}")

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Flask API is not running. "
            "Please start app.py first."
        )