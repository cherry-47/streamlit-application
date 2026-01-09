
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

st.set_page_config(page_title="Mood Score Predictor", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load("best_model.pkl")

model = load_model()

st.title("🧠 Lifestyle-Based Mood Score Prediction")
st.markdown("""
This application predicts **Mood Score** based on daily lifestyle habits.
It is designed for **ML competitions** with a clean UI, insights, and explainability.
""")

with st.sidebar:
    st.header("🔧 Input Your Daily Habits")
    sleep_hours = st.slider("Sleep Hours", 4.0, 10.0, 7.0)
    steps = st.number_input("Steps Walked", 0, 30000, 8000)
    calories = st.number_input("Calories Burned", 800, 5000, 2200)
    water = st.number_input("Water Intake (ml)", 500, 5000, 2500)
    study = st.slider("Study Hours", 0.0, 10.0, 4.0)
    wake_time = st.slider("Wake Up Hour", 4, 12, 7)
    day = st.slider("Day", 1, 31, 15)
    month = st.slider("Month", 1, 12, 6)
    weekday = st.slider("Weekday (0=Mon)", 0, 6, 2)

def prepare_input():
    sleep_cat_low = 1 if sleep_hours < 6 else 0
    sleep_cat_opt = 1 if 6 <= sleep_hours <= 8 else 0

    activity = steps + calories
    hydration = water / 1000
    study_effort = study * 10
    balance = sleep_hours*0.3 + hydration*0.2 + study*0.3 + activity*0.00005

    data = {
        "Sleep_Hours": sleep_hours,
        "Steps": steps,
        "Calories_Burned": calories,
        "Water_Intake_ml": water,
        "Study_Hours": study,
        "Wake_Up_Time": wake_time,
        "Day": day,
        "Month": month,
        "Weekday": weekday,
        "Activity_Score": activity,
        "Hydration_Liters": hydration,
        "Study_Effort": study_effort,
        "Lifestyle_Balance_Index": balance,
        "Sleep_Category_Low Sleep": sleep_cat_low,
        "Sleep_Category_Optimal Sleep": sleep_cat_opt
    }
    return pd.DataFrame([data])

input_df = prepare_input()

if st.button("🎯 Predict Mood Score"):
    prediction = model.predict(input_df)[0]
    st.success(f"### Predicted Mood Score: **{prediction} / 10**")

    fig = px.bar(
        x=["Sleep","Activity","Hydration","Study","Balance"],
        y=[sleep_hours, steps/1000, water/1000, study, input_df["Lifestyle_Balance_Index"][0]],
        title="Lifestyle Contribution Snapshot"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📊 How This Model Works")
st.markdown("""
- Trained on lifestyle & behavioral data
- Uses engineered features like **Lifestyle Balance Index**
- Best model selected via cross-validation
- Designed for **accuracy + interpretability**
""")

st.caption("© Competition-Ready ML Project | Streamlit Deployment")
