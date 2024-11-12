import os
import streamlit as st

import google.generativeai as genai

# Load environment variables


# Configure Gemini API using the API key from environment variable
genai.configure(api_key="AIzaSyBQIQFhqhphxHqiyu0VDMfkoCc2CEAIW6Y")

# Function to interact with the Gemini API and generate a response
def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content([prompt])
    return response.text

# Streamlit app configuration
st.set_page_config(page_title="Personalized Nutrition Chart App")
st.header("Personalized Nutrition Chart App")

# User input fields
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=1, max_value=120)
weight = st.number_input("Enter your weight (in kg):", min_value=1.0, max_value=300.0)
gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
activity_level = st.selectbox("Select your activity level:", ["Sedentary", "Lightly active", "Moderately active", "Very active", "Super active"])
timeframe = st.selectbox("Select the timeframe for your diet chart:", ["Day", "Week", "Month", "Year"])

# New: Dietary preference (Veg or Non-Veg)
diet_preference = st.selectbox("Select your dietary preference:", ["Vegetarian", "Non-Vegetarian"])

# Button to trigger the AI response
submit = st.button("Generate Diet Chart")

# If submit button is clicked
if submit:
    if not name or age == 0 or weight == 0:
        st.error("Please fill out all the fields.")
    else:
        # Update prompt according to user's input
        input_prompt = f"""
        You are a nutrition expert. Create a detailed {diet_preference.lower()} diet chart for {name}, a {age}-year-old {gender.lower()} weighing {weight} kg 
        with a(n) {activity_level.lower()} activity level. The diet chart should be for a {timeframe.lower()}.
        Ensure that the diet plan provides a balanced intake of proteins, carbohydrates, fats, vitamins, and minerals, 
        considering their age, weight, gender, and activity level. The diet should strictly follow {diet_preference.lower()} dietary guidelines.
        Include daily meal recommendations with portion sizes and nutritional information for each meal.provide csv file  
        """
        
        # Get the response from the AI
        response = get_gemini_response(input_prompt)
        
        # Display the response
        st.subheader(f"{diet_preference} Diet Chart for {timeframe}:")
        st.write(response)
