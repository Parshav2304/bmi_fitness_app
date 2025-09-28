import streamlit as st

def predict_plan(height, weight, age, gender, activity_level, body_fat):
    """Simple rule-based prediction - no ML model needed"""
    
    # Calculate BMI
    bmi = weight / ((height/100) ** 2)
    
    # Rule-based plan assignment
    if bmi < 18.5:
        return 'Bulk'
    elif bmi > 25:
        if body_fat > 25 or (body_fat > 20 and gender == 1):
            return 'Cut'
        else:
            return 'Recomp'
    elif age < 25 and activity_level > 1.5:
        return 'Lean'
    else:
        return 'Recomp'

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
    else:
        return int(tdee)

def macros_from_calories(calories, weight):
    protein_g = round(weight * 2.0)
    protein_kcal = protein_g * 4
    fat_kcal = int(calories * 0.25)
    fat_g = round(fat_kcal / 9)
    carbs_kcal = calories - (protein_kcal + fat_kcal)
    carbs_g = round(carbs_kcal / 4)
    
    return {'protein': protein_g, 'fat': fat_g, 'carbs': carbs_g}

# App UI
st.title('🏋️ Fitness AI App')

height = st.number_input('Height (cm)', min_value=100, value=170)
weight = st.number_input('Weight (kg)', min_value=30, value=70)
age = st.number_input('Age', min_value=10, value=25)
gender = st.selectbox('Gender', ['Female', 'Male'])
activity_level = st.selectbox('Activity Level', [1.2, 1.375, 1.55, 1.725, 1.9], index=2)
body_fat = st.number_input('Body Fat %', min_value=5
