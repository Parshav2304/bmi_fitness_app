# app/main.py
from fastapi import FastAPI # pyright: ignore[reportMissingImports]
from app.schemas import UserInput, PredictionOut # pyright: ignore[reportMissingImports]
from app.model import predict_plan # pyright: ignore[reportMissingImports]
from app import agent # pyright: ignore[reportMissingImports]

app = FastAPI(title='Fitness AI App')

# If using web frontend, enable CORS
from fastapi.middleware.cors import CORSMiddleware # pyright: ignore[reportMissingImports]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/predict', response_model=PredictionOut)
def predict(input: UserInput):
    if input.bmi is None:
        bmi_value = agent.calc_bmi(input.weight, input.height)
    else:
        bmi_value = input.bmi

    if input.body_fat is None:
        bf = (1.2 * bmi_value) + (0.23 * input.age) - (10.8 * input.gender) - 5.4
    else:
        bf = input.body_fat

    features = {
        'height': input.height,
        'weight': input.weight,
        'age': input.age,
        'gender': input.gender,
        'activity_level': input.activity_level,
        'body_fat': bf
    }

    plan = predict_plan(features)
    bmr = agent.bmr_mifflin(input.weight, input.height, input.age, input.gender)
    tdee = agent.tdee_from_bmr(bmr, input.activity_level)
    calories = agent.adjust_calories_for_plan(tdee, plan)
    macros = agent.macros_from_calories(calories, input.weight)
    return {
        'plan': plan,
        'bmi': round(bmi_value, 2),
        'tdee': round(tdee, 2),
        'calories': calories,
        'macros': macros,
        'notes': 'Plan predicted by ML; macros & calories by rule-based agent.'
    }
