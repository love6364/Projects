import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load best trained model, encoder, and feature names
with open("G:\\Final_Projects\\Machine_Learning\\Project2\\Food_Delivery_Time_Predictor\\Models\\best_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("G:\\Final_Projects\\Machine_Learning\\Project2\\Food_Delivery_Time_Predictor\\Models\\onehot_encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

with open("G:\\Final_Projects\\Machine_Learning\\Project2\\Food_Delivery_Time_Predictor\\Models\\encoded_feature_names.pkl", "rb") as f:
    encoded_feature_names = pickle.load(f)

# Streamlit UI
st.title("🚚 Food Delivery Time Predictor")

# User Inputs
distance_km = st.slider("📏 Delivery Distance (km)", 0.1, 50.0, 5.0)
preparation_time = st.slider("⏳ Preparation Time (minutes)", 1, 120, 15)
courier_experience = st.slider("👤 Courier Experience (years)", 0, 30, 5)

# Get categories from encoder
weather_options = encoder.categories_[0]
traffic_options = encoder.categories_[1]
time_of_day_options = encoder.categories_[2]
vehicle_options = encoder.categories_[3]

weather = st.selectbox("🌦️ Weather Conditions", weather_options)
traffic = st.selectbox("🚦 Traffic Level", traffic_options)
time_of_day = st.selectbox("⏰ Time of Day", time_of_day_options)
vehicle_type = st.selectbox("🚗 Vehicle Type", vehicle_options)

# One-Hot Encode input
input_df = pd.DataFrame([[weather, traffic, time_of_day, vehicle_type]], columns=["Weather", "Traffic_Level", "Time_of_Day", "Vehicle_Type"])
encoded_input = encoder.transform(input_df)
encoded_input_df = pd.DataFrame(encoded_input, columns=encoded_feature_names)

# Create feature array
input_data = np.array([[
    distance_km,
    preparation_time,
    courier_experience,
    *encoded_input_df.iloc[0].values  # Ensure correct feature alignment
]])

# Debugging: Show input shape
st.write(f"🔍 Input Shape: {input_data.shape}")

# Make prediction
pred = model.predict(input_data)[0]

# Display result
st.subheader(f"⏱️ Estimated Delivery Time: **{int(pred)} minutes**")