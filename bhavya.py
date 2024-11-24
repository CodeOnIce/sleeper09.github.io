import streamlit as st
import google.generativeai as genai
import pandas as pd

genai.configure(api_key="AIzaSyDQXlrtFcl_3z_nMHJQrLWUYbnmNURpOSk")

# Function to generate a response using the Gemini API
def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content([prompt])
    return response.text

# Function to parse AI response into a structured table and text
def parse_response(response):
    table_rows = []
    other_details = []
    lines = response.splitlines()
    
    for line in lines:
        if ':' in line and 'Meal' in line:
            # Check for table entries (e.g., "Meal: Breakfast, Calories: 300, Time: 8:00 AM")
            parts = line.split(',')
            entry = {part.split(':')[0].strip(): part.split(':')[1].strip() for part in parts}
            table_rows.append(entry)
        else:
            # Collect other text information
            other_details.append(line)
    
    return pd.DataFrame(table_rows), '\n'.join(other_details)

# Streamlit app configuration
st.set_page_config(page_title="Personalized Nutrition Chart App")
st.header("Personalized Nutrition Chart App")

# User input fields
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=1, max_value=120)
height = st.number_input("Enter your height (in cm):", min_value=50.0, max_value=250.0)
weight = st.number_input("Enter your weight (in kg):", min_value=1.0, max_value=300.0)
gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
activity_level = st.selectbox("Select your activity level:", ["Sedentary", "Lightly active", "Moderately active", "Very active", "Super active"])
timeframe = st.selectbox("Select the timeframe for your diet chart:", ["Day", "Week", "Month", "Year"])

# Dietary preference and allergies
diet_preference = st.selectbox("Select your dietary preference:", ["Vegetarian", "Non-Vegetarian"])
allergies = st.text_input("Enter any food items you are allergic to (comma-separated):")

# Purpose of the diet chart
purpose = st.selectbox("What is the purpose of this diet chart?", ["Weight Loss", "Weight Gain", "Muscle Building"])

# Calculate BMI
if height > 0:
    bmi = round(weight / ((height / 100) ** 2), 2)
    st.write(f"Your BMI: {bmi}")

# Button to trigger the AI response
submit = st.button("Generate Diet Chart")

# If submit button is clicked
if submit:
    if not name or age == 0 or weight == 0 or height == 0:
        st.error("Please fill out all the fields.")
    else:
        # Update prompt according to user's input
        input_prompt = f"""
        You are a nutrition expert. Create a detailed {diet_preference.lower()} diet chart for {name}, a {age}-year-old {gender.lower()} 
        weighing {weight} kg, {height} cm tall, with a BMI of {bmi}, and a(n) {activity_level.lower()} activity level. 
        The diet chart should be for a {timeframe.lower()}.

        The goal of this diet chart is {purpose.lower()}. Ensure that the recommendations align with this goal and provide a 
        balanced intake of proteins, carbohydrates, fats, vitamins, and minerals, considering their age, weight, height, gender, 
        activity level, and BMI. Strictly follow {diet_preference.lower()} dietary guidelines.

        Exclude any foods that contain: {allergies}.
        
        Include daily meal recommendations with portion sizes, calories, and the ideal time to consume each meal. Output the meal 
        details in a structured table with columns "Meal", "Calories", and "Time". Include additional suggestions or tips in normal text format.
        """

        # Get the response from the AI
        response = get_gemini_response(input_prompt)
        
        # Parse the response into a table and text
        diet_chart_table, additional_details = parse_response(response)
        
        # Display the response in table format and text format
        st.subheader(f"{diet_preference} Diet Chart for {purpose} ({timeframe}):")
        st.table(diet_chart_table)

        st.subheader("Additional Suggestions and Tips:")
        st.write(additional_details)

        # Generate a CSV for download
        csv = diet_chart_table.to_csv(index=False)
        st.download_button(
            label="Download Diet Chart as CSV",
            data=csv,
            file_name=f"{name}_{timeframe}_diet_chart.csv",
            mime="text/csv"
        )
