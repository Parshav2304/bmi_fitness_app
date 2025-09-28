import streamlit as st

def predict_plan(height, weight, age, gender, activity_level, body_fat):
    """Rule-based fitness plan prediction"""
    
    # Calculate BMI
    bmi = weight / ((height/100) ** 2)
    
    # Rule-based plan assignment
    if bmi < 18.5:
        return 'Bulking'
    elif bmi > 25:
        if body_fat > 25 or (body_fat > 20 and gender == 1):
            return 'Cutting'
        else:
            return 'Body Recomp'
    elif age < 25 and activity_level > 1.5:
        return 'Lean Bulk'
    else:
        return 'Body Recomp'

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
    if plan == 'Cutting':
        return int(tdee - 500)
    elif plan == 'Bulking':
        return int(tdee + 400)
    elif plan == 'Lean Bulk':
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

# Streamlit App
st.title('🏋️ Fitness AI App')
st.write("Get personalized fitness recommendations based on your body metrics!")

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
        bf = max(5, min(bf, 40))  # Keep within reasonable bounds
    else:
        bf = body_fat
    
    # Make prediction
    gender_num = 1 if gender == 'Male' else 0
    plan = predict_plan(height, weight, age, gender_num, activity_level, bf)
    
    # Calculate nutrition metrics
    bmr = bmr_mifflin(weight, height, age, gender_num)
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
            'Cutting': '✂️',
            'Bulking': '💪',
            'Lean Bulk': '🎯',
            'Body Recomp': '🔄'
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
        'Cutting': "Focus on fat loss while preserving muscle mass. Maintain a caloric deficit with adequate protein intake.",
        'Bulking': "Build muscle mass and strength. Increase calories with emphasis on protein and complex carbs.",
        'Lean Bulk': "Slow, controlled muscle gain while minimizing fat gain. Moderate caloric surplus.",
        'Body Recomp': "Body recomposition - lose fat and gain muscle simultaneously. Maintain calories at TDEE level."
    }
    
    st.info(plan_descriptions.get(plan, "Follow a balanced approach to nutrition and training."))
    
    # BMI interpretation
    if bmi_value < 18.5:
        st.warning("⚠️ Your BMI indicates you may be underweight. Consider consulting with a healthcare provider.")
    elif bmi_value > 25:
        st.warning("⚠️ Your BMI indicates you may be overweight. The plan focuses on healthy weight management.")
    else:
        st.success("✅ Your BMI is in the normal range!")
    
    # Additional notes
    st.write("---")
    st.caption("💡 **Note:** This plan uses evidence-based calculations and rule-based recommendations. For personalized advice, consult with a qualified nutritionist or trainer.")

# Sidebar with information
st.sidebar.header("ℹ️ About This App")
st.sidebar.info(
    "This fitness app calculates your:\n"
    "- BMI (Body Mass Index)\n"
    "- BMR (Basal Metabolic Rate)\n"
    "- TDEE (Total Daily Energy Expenditure)\n"
    "- Personalized fitness plan\n"
    "- Macro nutrient targets"
)

st.sidebar.header("📚 Activity Levels")
st.sidebar.text("""
Sedentary: Desk job, no exercise
Light: Light exercise 1-3 days/week
Moderate: Exercise 3-5 days/week
Active: Exercise 6-7 days/week
Very Active: 2x/day or physical job
""")


