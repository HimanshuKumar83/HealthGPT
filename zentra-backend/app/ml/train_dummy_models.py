import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.ensemble import RandomForestClassifier
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

label_encoders = {
    'gender': LabelEncoder().fit(['Male', 'Female']),
    'family_history': LabelEncoder().fit(['yes', 'no']),
    'high_calorie_food': LabelEncoder().fit(['yes', 'no']),
    'smoking': LabelEncoder().fit(['yes', 'no']),
    'monitor_calories': LabelEncoder().fit(['yes', 'no'])
}
joblib.dump(label_encoders, os.path.join(BASE_DIR, "label_encoders.pkl"))

target_encoder = LabelEncoder().fit(['Normal_Weight', 'Overweight_Level_I', 'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III', 'Insufficient_Weight'])
joblib.dump(target_encoder, os.path.join(BASE_DIR, "target_label_encoder.pkl"))

scaler = RobustScaler()
num_cols = [
    'age', 'height_m', 'weight_kg', 'bmi',
    'vegetable_intake_freq', 'main_meals_per_day',
    'water_intake_liters', 'physical_activity_hours',
    'screentime_hours'
]
dummy_num = pd.DataFrame(np.random.rand(10, len(num_cols)), columns=num_cols)
scaler.fit(dummy_num)
joblib.dump(scaler, os.path.join(BASE_DIR, "robust_scaler.pkl"))

feature_columns = num_cols + ['gender', 'family_history', 'high_calorie_food', 'smoking', 'monitor_calories', 
                              'snack_frequency_Frequently', 'snack_frequency_Sometimes', 'snack_frequency_no', 'snack_frequency_Always',
                              'alcohol_consumption_Frequently', 'alcohol_consumption_Sometimes', 'alcohol_consumption_no', 'alcohol_consumption_Always',
                              'travel_mode_Automobile', 'travel_mode_Motorbike', 'travel_mode_Bike', 'travel_mode_Public_Transportation', 'travel_mode_Walking']
joblib.dump(feature_columns, os.path.join(BASE_DIR, "feature_columns.pkl"))

model = RandomForestClassifier()
X = pd.DataFrame(np.random.rand(10, len(feature_columns)), columns=feature_columns)
y = np.random.randint(0, 7, 10)
model.fit(X, y)
joblib.dump(model, os.path.join(BASE_DIR, "random_forest_model.pkl"))
print("Dummy models created.")
