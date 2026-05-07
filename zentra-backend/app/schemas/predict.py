from pydantic import BaseModel
from typing import Literal

class PredictionRequest(BaseModel):

    gender: Literal["Male", "Female"] = "Female"

    age: float = 25.0
    height_m: float = 1.65
    weight_kg: float = 65.0

    family_overweight_history: Literal["yes", "no"] = "no"
    high_calorie_food: Literal["yes", "no"] = "no"

    vegetable_intake_freq: float = 2.0
    main_meals_per_day: float = 3.0

    snack_frequency: Literal["no", "Sometimes", "Frequently"] = "Sometimes"
    smokes: Literal["yes", "no"] = "no"

    water_intake_liters: float = 2.0
    calorie_tracking: Literal["yes", "no"] = "no"

    physical_activity_hours: float = 0.5
    screentime_hours: float = 4.0

    alcohol_consumption: Literal["no", "Sometimes", "Frequently"] = "no"

    travel_mode: Literal[
        "Car",
        "Walking",
        "Bike",
        "Motorbike",
        "Public_Transportation"
    ] = "Public_Transportation"

class PredictionResponse(BaseModel):
    obesity_level:str
