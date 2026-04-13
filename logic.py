import json
import random
from typing import List, Dict
from models import UserProfile, Meal, CalorieMacros, DailyPlan

def calculate_targets(profile: UserProfile) -> CalorieMacros:
    # Mifflin-St Jeor Equation
    if profile.gender.lower() == 'male':
        bmr = 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age + 5
    else:
        bmr = 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age - 161
    
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    tdee = bmr * activity_multipliers.get(profile.activity_level, 1.2)
    
    if profile.goal == 'weight_loss':
        target_calories = tdee - 500
    elif profile.goal == 'muscle_gain':
        target_calories = tdee + 300
    else:
        target_calories = tdee
        
    # Macros distribution: 30% Protein, 40% Carbs, 30% Fat
    protein_g = (target_calories * 0.30) / 4
    carbs_g = (target_calories * 0.40) / 4
    fat_g = (target_calories * 0.30) / 9
    
    return CalorieMacros(
        calories=int(target_calories),
        protein=int(protein_g),
        carbs=int(carbs_g),
        fat=int(fat_g)
    )

def generate_meal_plan(profile: UserProfile, meals_db: List[dict]) -> DailyPlan:
    # 1. Filter by Allergens
    safe_meals = [
        m for m in meals_db 
        if not any(allergy.lower() in [a.lower() for a in m['allergens']] for allergy in profile.allergies)
    ]
    
    targets = calculate_targets(profile)
    
    # Simple split: Breakfast 25%, Lunch 35%, Dinner 30%, Snack 10%
    splits = {
        'Breakfast': 0.25,
        'Lunch': 0.35,
        'Dinner': 0.30,
        'Snack': 0.10
    }
    
    plan_meals = {}
    
    for category, weight in splits.items():
        cat_meals = [m for m in safe_meals if m['category'] == category]
        target_cat_cals = targets.calories * weight
        
        # Rank by calories proximity
        cat_meals.sort(key=lambda x: abs(x['calories'] - target_cat_cals))
        
        # Select best match (with small randomization from top 3 for diversity)
        selection_pool = cat_meals[:3] if len(cat_meals) >= 3 else cat_meals
        plan_meals[category.lower()] = Meal(**random.choice(selection_pool))
        
    total_c = sum(m.calories for m in plan_meals.values())
    total_p = sum(m.protein for m in plan_meals.values())
    total_cb = sum(m.carbs for m in plan_meals.values())
    total_f = sum(m.fat for m in plan_meals.values())
    
    return DailyPlan(
        breakfast=plan_meals['breakfast'],
        lunch=plan_meals['lunch'],
        dinner=plan_meals['dinner'],
        snack=plan_meals['snack'],
        total_metrics=CalorieMacros(calories=total_c, protein=total_p, carbs=total_cb, fat=total_f)
    )
