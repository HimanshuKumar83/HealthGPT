from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.predict import PredictionRequest, PredictionResponse
from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.db import models

from app.ml.inference_pipeline import predict_obesity

router = APIRouter(prefix="/predict", tags=["Predictions"])

@router.post("/", response_model=PredictionResponse)
async def predict_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 1. Fetch user health profile
    result = await db.execute(
        select(models.UserHealthProfile).filter(
            models.UserHealthProfile.user_id == current_user.id
        )
    )
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=400,
            detail="Health profile not found. Please create your profile first."
        )

    # 2. Convert SQLAlchemy model → dict for inference pipeline
    travel_mode_mapping = {
        "Car": "Automobile",
        "Walking": "Walking",
        "Bike": "Bike",
        "Motorbike": "Motorbike",
        "Public_Transportation": "Public_Transportation"
    }

    user_input = {
        "gender": profile.gender,
        "age": profile.age,
        "height_m": profile.height_m,
        "weight_kg": profile.weight_kg,
        "bmi": profile.bmi,  # optional, depends on pipeline

        "family_history": profile.family_overweight_history,
        "high_calorie_food": profile.high_calorie_food,

        "vegetable_intake_freq": profile.vegetable_intake_freq,
        "main_meals_per_day": profile.main_meals_per_day,

        "snack_frequency": profile.snack_frequency,
        "smoking": profile.smokes,

        "water_intake_liters": profile.water_intake_liters,
        "monitor_calories": profile.calorie_tracking,

        "physical_activity_hours": profile.physical_activity_hours,
        "screentime_hours": profile.screentime_hours,

        "alcohol_consumption": profile.alcohol_consumption,
        "travel_mode": travel_mode_mapping.get(profile.travel_mode, profile.travel_mode),
    }

    # 3. Run the ML model (synchronous - FastAPI handles in thread pool)
    prediction_label = predict_obesity(user_input)

    # 4. Store prediction history
    record = models.PredictionHistory(
        user_id=current_user.id,
        input_data=str(user_input),
        prediction=prediction_label
    )

    db.add(record)
    await db.commit()

    return PredictionResponse(obesity_level=prediction_label)

