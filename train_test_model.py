import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import xgboost as xgb
import joblib
import os

# Load dataset - update this path to your actual dataset location
df = pd.read_csv('fitness_dataset.csv')

# Features and target
feature_cols = ['Height', 'Weight', 'Age', 'Gender', 'Activity_Level', 'Body_Fat']
x = df[feature_cols]
y = df['Plan']

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Train XGBoost model - fixed typo in XGBClassifier
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
model.fit(x_train, y_train)

# Save model
joblib.dump(model, 'plan_predictor.pkl')
print("Model trained and saved to plan_predictor.pkl")

# Print accuracy
from sklearn.metrics import accuracy_score
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.2f}")