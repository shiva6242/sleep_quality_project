import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("sleep_model.pkl")

st.title("🛌 Sleep Quality Predictor")
st.write("Predict sleep quality based on lifestyle factors")

# User inputs
screen_time = st.slider("Screen Time (hours)", 1.0, 10.0, 5.0)
age = st.slider("Age", 18, 60, 30)
activity = st.slider("Physical Activity (minutes)", 0, 120, 30)
caffeine = st.slider("Caffeine Intake (cups/day)", 0, 5, 1)

# Feature engineering (same as training)
screen_activity_ratio = screen_time / (activity + 1)
high_caffeine = 1 if caffeine >= 3 else 0

# Categorize activity
if activity < 30:
    activity_level = "Low"
elif activity < 60:
    activity_level = "Moderate"
else:
    activity_level = "High"

# Categorize screen time
if screen_time < 3:
    screen_category = "Low"
elif screen_time < 6:
    screen_category = "Medium"
elif screen_time < 8:
    screen_category = "High"
else:
    screen_category = "Very High"

# Base input dataframe (MATCH TRAINING COLUMN NAMES)
input_data = pd.DataFrame({
    "Age": [age],
    "Screen_Time_Hours": [screen_time],
    "Physical_Activity_Min": [activity],
    "Caffeine_Intake": [caffeine],
    "Screen_Activity_Ratio": [screen_activity_ratio],
    "High_Caffeine": [high_caffeine]
})

# Dummy columns (same as training)
activity_cols = [
    "Activity_Level_Low",
    "Activity_Level_Moderate",
    "Activity_Level_High"
]

screen_cols = [
    "Screen_Time_Category_Low",
    "Screen_Time_Category_Medium",
    "Screen_Time_Category_High",
    "Screen_Time_Category_Very High"
]

# Initialize all dummy columns with 0
for col in activity_cols + screen_cols:
    input_data[col] = 0

# Set correct category to 1
input_data[f"Activity_Level_{activity_level}"] = 1
input_data[f"Screen_Time_Category_{screen_category}"] = 1

# Align columns exactly with model
input_data = input_data[model.feature_names_in_]

# Prediction
if st.button("Predict Sleep Quality"):
    prediction = model.predict(input_data)[0]
    st.success(f"Predicted Sleep Quality Score: {prediction:.2f}")
