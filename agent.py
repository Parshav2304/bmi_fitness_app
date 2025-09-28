def calc_bmi(weight_kg, height_cm):
    # Calculate BMI from weight (kg) and height (cm)
    h = height_cm / 100
    return weight_kg / (h * h)

def bmr_mifflin(weight, height, age, gender):
    # """Calculate BMR using Mifflin-St Jeor equation"""
    if gender == 1:  # Male
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:  # Female
        return 10 * weight + 6.25 * height - 5 * age - 161

def tdee_from_bmr(bmr, activity_level):
    # """Calculate TDEE from BMR and activity level"""
    return bmr * activity_level

def adjust_calories_for_plan(tdee, plan):
    # """Adjust calories based on fitness plan"""
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
    # """Calculate macro distribution from calories and weight"""
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