import joblib # type: ignore
import numpy as np
import pandas as pd # type: ignore
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

label_encoders = joblib.load(os.path.join(BASE_DIR, "label_encoders.pkl"))
target_encoder = joblib.load(os.path.join(BASE_DIR, "target_label_encoder.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "robust_scaler.pkl"))
feature_columns = joblib.load(os.path.join(BASE_DIR, "feature_columns.pkl"))
model = joblib.load(os.path.join(BASE_DIR, "random_forest_model.pkl"))

def preprocess_input(user_input: dict)-> pd.DataFrame:
    df=pd.DataFrame([user_input])
    df["bmi"] = df["weight_kg"] / (df["height_m"] ** 2)
    for col, encoder in label_encoders.items():
        df[col] = encoder.transform(df[col])
    df = pd.get_dummies(df, columns=["snack_frequency", "alcohol_consumption", "travel_mode"])
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0
    df = df[feature_columns]
    num_cols = [
    'age', 'height_m', 'weight_kg', 'bmi',
    'vegetable_intake_freq', 'main_meals_per_day',
    'water_intake_liters', 'physical_activity_hours',
    'screentime_hours'
    ]
    df[num_cols] = scaler.transform(df[num_cols])
    return df

    

def predict_obesity(user_input:dict)->str:
    processed = preprocess_input(user_input)
    pred = model.predict(processed)[0]
    label = target_encoder.inverse_transform([pred])[0]
    return label
