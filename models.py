from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    goal: str  # 'weight_loss', 'maintenance', 'muscle_gain'
    dietary_preferences: List[str]
    allergies: List[str]
    activity_level: str  # 'sedentary', 'light', 'moderate', 'active', 'very_active'

class CalorieMacros(BaseModel):
    calories: int
    protein: int
    carbs: int
    fat: int

class Meal(BaseModel):
    id: int
    name: str
    category: str
    calories: int
    protein: int
    carbs: int
    fat: int
    allergens: List[str]
    description: str

class DailyPlan(BaseModel):
    breakfast: Meal
    lunch: Meal
    dinner: Meal
    snack: Meal
    total_metrics: CalorieMacros
