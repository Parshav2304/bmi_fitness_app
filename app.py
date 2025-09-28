import streamlit as st
import joblib
import numpy as np
import os

# Load model
@st.cache_resource
def load_model():
    try:
        model = joblib.load('plan_predictor.pkl')
        return model
    except FileNotFoundError:
        st.error("Model file 'plan_predictor.pkl' not found. Please train the model first.")
        return None

def calc_bmi(weight_kg, height_cm):
    h = height_cm / 100
    return weight_kg / (h * h)

def bmr_mifflin(weight, height, age, gender):
    if gender == 1:  # Male
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:  # Female
        return 10 * weight + 6.25 * height - 5 * age - 161

def tdee_from_bmr(bmr, activity_level):
    return bmr * activity_level

def adjust_calories_for_plan(tdee, plan):
    if plan == 'Cut':
        return int(tdee - 500)
    elif plan == 'Bulk':
        return int(tdee + 400)
    elif plan == 'Lean':
        return int(tdee + 150)
    elif plan == 'Recomp':
        return int(tdee)
    else:
        return int(tdee)

def macros_from_calories(calories, weight, protein_g_per_kg=2.0, fat_pct=0.25):
    protein_g = round(weight * protein_g_per_kg)
    protein_kcal = protein_g * 4
    fat_kcal = int(calories * fat_pct)
    fat_g = round(fat_kcal / 9)
    carbs_kcal = calories - (protein_kcal + fat_kcal)
    carbs_g = round(carbs_kcal / 4)
    
    return {
        'protein': protein_g,
        'fat': fat_g,
        'carbs': carbs_g
    }

def predict_plan(features, model):
    X = [[features['height'], features['weight'], features['age'], 
          features['gender'], features['activity_level'], features['body_fat']]]
    pred = model.predict(X)[0]
    return pred

# Streamlit UI
st.title('🏋️ Fitness AI App')
st.write("Get personalized fitness recommendations based on your body metrics!")

# Load model
model = load_model()

if model is not None:
    # Input fields
    col1, col2 = st.columns(2)
    
    with col1:
        height = st.number_input('Height (cm)', min_value=100, max_value=250, value=170)
        weight = st.number_input('Weight (kg)', min_value=30, max_value=200, value=70)
        age = st.number_input('Age', min_value=10, max_value=100, value=25)
    
    with col2:
        gender = st.selectbox('Gender', options=['Female', 'Male'])
        activity_level = st.selectbox(
            'Activity Level',
            options=[1.2, 1.375, 1.55, 1.725, 1.9],
            format_func=lambda x: {
                1.2: 'Sedentary (little/no exercise)',
                1.375: 'Light (light exercise 1-3 days/week)',
                1.55: 'Moderate (moderate exercise 3-5 days/week)',
                1.725: 'Active (hard exercise 6-7 days/week)',
                1.9: 'Very Active (very hard exercise, physical job)'
            }[x],
            index=2
        )
        body_fat = st.number_input('Body Fat % (optional)', min_value=0.0, max_value=50.0, value=0.0)

    if st.button('🎯 Get Your Fitness Plan', type="primary"):
        # Calculate BMI
        bmi_value = calc_bmi(weight, height)
        
        # Estimate body fat if not provided
        if body_fat == 0.0:
            gender_num = 1 if gender == 'Male' else 0
            bf = (1.2 * bmi_value) + (0.23 * age) - (10.8 * gender_num) - 5.4
        else:
            bf = body_fat
        
        # Prepare features
        features = {
            'height': height,
            'weight': weight,
            'age': age,
            'gender': 1 if gender == 'Male' else 0,
            'activity_level': activity_level,
            'body_fat': bf
        }
        
        # Make prediction
        plan = predict_plan(features, model)
        
        # Calculate nutrition metrics
        bmr = bmr_mifflin(weight, height, age, features['gender'])
        tdee = tdee_from_bmr(bmr, activity_level)
        calories = adjust_calories_for_plan(tdee, plan)
        macros = macros_from_calories(calories, weight)
        
        # Display results
        st.success('🎉 Your Personalized Fitness Plan is Ready!')
        
        # Create metrics display
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("BMI", f"{bmi_value:.1f}")
        with col2:
            st.metric("TDEE", f"{tdee:.0f} kcal")
        with col3:
            st.metric("Target Calories", f"{calories} kcal")
        with col4:
            plan_emoji = {
                'Cut': '✂️',
                'Bulk': '💪',
                'Lean': '🎯',
                'Recomp': '🔄'
            }
            st.metric("Plan", f"{plan_emoji.get(plan, '📋')} {plan}")
        
        # Macro breakdown
        st.subheader("📊 Daily Macro Targets")
        macro_col1, macro_col2, macro_col3 = st.columns(3)
        
        with macro_col1:
            st.metric("Protein", f"{macros['protein']}g", help="For muscle building and repair")
        with macro_col2:
            st.metric("Carbs", f"{macros['carbs']}g", help="For energy and performance")
        with macro_col3:
            st.metric("Fat", f"{macros['fat']}g", help="For hormone production and absorption")
        
        # Plan explanation
        st.subheader("📝 Plan Details")
        plan_descriptions = {
            'Cut': "Focus on fat loss while preserving muscle mass. Maintain a caloric deficit with adequate protein intake.",
            'Bulk': "Build muscle mass and strength. Increase calories with emphasis on protein and complex carbs.",
            'Lean': "Slow, controlled muscle gain while minimizing fat gain. Moderate caloric surplus.",
            'Recomp': "Body recomposition - lose fat and gain muscle simultaneously. Maintain calories at TDEE level."
        }
        
        st.info(plan_descriptions.get(plan, "Follow a balanced approach to nutrition and training."))
        
        # Additional notes
        st.write("---")
        st.caption("💡 **Note:** This plan is generated by machine learning based on your input data. For personalized advice, consult with a qualified nutritionist or trainer.")

else:
    st.error("Please ensure the model file 'plan_predictor.pkl' is available in the app directory.")