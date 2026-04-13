const API_URL = "http://localhost:8000";

// DOM Elements
const onboardingForm = document.getElementById('onboarding-form');
const onboardingView = document.getElementById('onboarding');
const dashboardView = document.getElementById('dashboard');
const navbar = document.getElementById('navbar');
const mealList = document.getElementById('meal-list');

// Progress Elements
const calsVal = document.getElementById('cals-val');
const proteinVal = document.getElementById('protein-val');
const carbsVal = document.getElementById('carbs-val');
const fatVal = document.getElementById('fat-val');
const progressBar = document.getElementById('progress-bar');

onboardingForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const profile = {
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        height_cm: parseFloat(document.getElementById('height').value),
        weight_kg: parseFloat(document.getElementById('weight').value),
        goal: document.getElementById('goal').value,
        activity_level: document.getElementById('activity').value,
        dietary_preferences: [],
        allergies: document.getElementById('allergies').value.split(',').map(s => s.trim()).filter(s => s)
    };

    try {
        // 1. Save Profile
        const res = await fetch(`${API_URL}/profile`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profile)
        });
        
        if (!res.ok) throw new Error('Failed to save profile');
        
        // 2. Get Meal Plan
        const planRes = await fetch(`${API_URL}/plan`);
        const plan = await planRes.json();
        
        renderDashboard(plan);
        switchView('dashboard');
    } catch (err) {
        console.error(err);
        alert('Error connecting to backend. Make sure the FastAPI server is running!');
    }
});

function switchView(viewId) {
    onboardingView.classList.add('hidden');
    dashboardView.classList.add('hidden');
    
    document.getElementById(viewId).classList.remove('hidden');
    if (viewId === 'dashboard') navbar.classList.remove('hidden');
}

function renderDashboard(plan) {
    const { total_metrics, breakfast, lunch, dinner, snack } = plan;
    
    // Update Stats
    calsVal.textContent = total_metrics.calories;
    proteinVal.textContent = `${total_metrics.protein}g`;
    carbsVal.textContent = `${total_metrics.carbs}g`;
    fatVal.textContent = `${total_metrics.fat}g`;
    
    // Animate Progress Bar (SVG dashoffset)
    // 440 is the circumference (2 * PI * 70)
    progressBar.style.strokeDashoffset = 0; 

    // Render Meals
    const meals = [
        { ...breakfast, time: 'Breakfast' },
        { ...lunch, time: 'Lunch' },
        { ...dinner, time: 'Dinner' },
        { ...snack, time: 'Snack' }
    ];
    
    mealList.innerHTML = meals.map(meal => `
        <div class="meal-card">
            <div class="meal-img" style="background: linear-gradient(135deg, #1e293b, #334155); display: flex; align-items: center; justify-content: center; font-size: 2rem;">
                ${getCategoryEmoji(meal.category)}
            </div>
            <div class="meal-info">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <span class="meal-meta">${meal.time}</span>
                    <span style="font-size: 0.75rem; color: var(--primary); font-weight: 700;">${meal.calories} kcal</span>
                </div>
                <div class="meal-name">${meal.name}</div>
                <div class="meal-meta">${meal.protein}g Protein • ${meal.carbs}g Carbs</div>
            </div>
            <div style="color: var(--text-dim); cursor: pointer;">⋮</div>
        </div>
    `).join('');
}

function getCategoryEmoji(cat) {
    const emojis = {
        'Breakfast': '🍳',
        'Lunch': '🥗',
        'Dinner': '🥩',
        'Snack': '🍎'
    };
    return emojis[cat] || '🍽️';
}
