
import os
import requests
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

# =========================
# LOAD .ENV FILE
# =========================
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_URL = os.getenv("API_URL")

# =========================
# STREAMLIT CONFIG
# =========================
st.set_page_config(
    page_title="MedBuddy.ML",
    page_icon="⚕️",
    layout="centered"
)

# =========================
# TITLE
# =========================
st.title("⚕️ MedBuddy.ML")
st.write("Heart Disease Risk Predictor")

# Debugging (optional)
# st.write("API URL:", API_URL)

# =========================
# INPUT FORM
# =========================
st.subheader("Enter patient details and click Predict")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", 1, 120, 52)
    sex = st.selectbox("Sex (1 = Male, 0 = Female)", [0, 1])
    cp = st.number_input("Chest Pain Type (cp)", 0, 3, 0)
    trestbps = st.number_input("Resting Blood Pressure", 0, 250, 125)
    chol = st.number_input("Cholesterol", 0, 600, 212)

with col2:
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1])
    restecg = st.number_input("Resting ECG (restecg)", 0, 2, 1)
    thalach = st.number_input("Max Heart Rate (thalach)", 0, 250, 168)
    exang = st.selectbox("Exercise Induced Angina", [0, 1])

with col3:
    oldpeak = st.number_input("Oldpeak (ST depression)", 0.0, 10.0, 1.0)
    slope = st.number_input("Slope", 0, 2, 2)
    ca = st.number_input("Number of Major Vessels (ca)", 0, 4, 0)
    thal = st.number_input("Thal", 0, 3, 2)

# =========================
# PREDICT BUTTON
# =========================
if st.button("🔍 Predict"):

    # check API URL
    if not API_URL:
        st.error("API_URL not found in .env file")
        st.stop()

    # input data
    input_data = {
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal
    }

    try:
        # send request
        response = requests.post(API_URL, json=input_data)

        # check status
        if response.status_code != 200:
            st.error("Something went wrong. Backend API error.")

        else:
            result = response.json()

            prediction = result["prediction"]
            probability = result["probability"]
            diagnosis = result["diagnosis"]

            st.divider()

            st.metric(
                label="Heart Disease Probability",
                value=f"{probability:.2f}"
            )

            if prediction == 1:
                st.error(f"⚠️ Model Prediction: {diagnosis}")
            else:
                st.success(f"✅ Model Prediction: {diagnosis}")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to FastAPI backend. Make sure backend server is running.")

    except Exception as e:
        st.error(f"Error: {e}")

