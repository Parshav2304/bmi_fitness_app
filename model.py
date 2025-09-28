import joblib # pyright: ignore[reportMissingImports]
import numpy as np # pyright: ignore[reportMissingImports]
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'plan_predictor.pkl')

def load_model():
    model = joblib.load(MODEL_PATH)
    return model

MODEL = load_model()

def predict_plan(features: dict):
    X = [[features['height'], features['weight'],features['age'], features['gender'], features['activity_level'], features['body_fat']]]
    pred = MODEL.predict(X)[0]
    return pred


