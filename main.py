from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import json
import os
from models import UserProfile, DailyPlan, Meal
from logic import generate_meal_plan, calculate_targets

app = FastAPI(title="NutriSync API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory=".", html=True), name="static")

MEALS_FILE = "meals.json"

def load_meals():
    if not os.path.exists(MEALS_FILE):
        return []
    with open(MEALS_FILE, "r") as f:
        return json.load(f)

# Mock DB for session (In-memory for MVP)
current_profile = None

@app.post("/profile")
async def save_profile(profile: UserProfile):
    global current_profile
    current_profile = profile
    targets = calculate_targets(profile)
    return {"status": "success", "targets": targets}

@app.get("/plan", response_model=DailyPlan)
async def get_plan():
    global current_profile
    if not current_profile:
        raise HTTPException(status_code=400, detail="Profile not set")
    
    meals_db = load_meals()
    plan = generate_meal_plan(current_profile, meals_db)
    return plan

@app.get("/meals", response_model=List[Meal])
async def search_meals(query: str = ""):
    meals_db = load_meals()
    if not query:
        return [Meal(**m) for m in meals_db]
    
    results = [
        Meal(**m) for m in meals_db 
        if query.lower() in m['name'].lower() or query.lower() in m['description'].lower()
    ]
    return results

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
