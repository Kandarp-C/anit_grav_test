# NutriSync — Requirements Specification (MVP)

## 1. Introduction

### 1.1 Purpose
This document defines the functional and non-functional requirements for the NutriSync MVP.

### 1.2 Product Summary
NutriSync is an AI-powered mobile health application that provides personalized meal recommendations, tracking, and engagement.

---

## 2. Scope (MVP)

### Included
- User onboarding & profile
- Meal recommendation engine
- Meal logging
- Progress tracking
- Gamification
- Notifications

### Excluded
- Wearables
- Social features
- Telehealth
- Grocery integration
- Barcode scanning

---

## 3. Functional Requirements

### 3.1 User Onboarding & Profile
- Email/password & OAuth login
- Email verification
- Profile inputs:
  - Age, gender, height, weight
  - Goals
  - Dietary preferences
  - Allergies
  - Activity level
- Calorie & macro calculation
- Editable profile

---

### 3.2 Meal Recommendation Engine
- Daily meal plan generation
- Personalized recommendations
- Allergen avoidance
- Macro & calorie matching (±10%)
- Meal swapping (max 3/day)
- Feedback system (ratings)

---

### 3.3 Meal Logging
- Log meals via:
  - Recommendations
  - Search
- Portion control
- Nutrition calculation
- Edit/delete logs
- Water tracking

---

### 3.4 Progress Tracking
- Dashboard with:
  - Meal plan
  - Macro progress
  - Streaks
- Charts:
  - Weekly/monthly trends
- Weight tracking
- Consistency score

---

### 3.5 Gamification
- Points system
- Levels
- Streaks
- Badges
- Weekly challenges

---

### 3.6 Notifications
- Morning plan notification
- Meal reminders
- Streak alerts
- Weekly summary

---

### 3.7 Settings
- Profile editing
- Credential updates
- Account deletion
- Notification controls
- Dark mode

---

## 4. Non-Functional Requirements

### Performance
- App launch < 3s
- Recommendations < 2s
- Search < 1s

### Security
- TLS encryption
- Secure password hashing
- Data encryption at rest
- GDPR & DPDPA compliance

### Usability
- ≤ 2 taps for key actions
- Accessible UI
- High usability score

### Scalability
- Support 100k users
- Horizontal scaling

### Reliability
- Offline mode support
- Daily backups

---

## 5. Architecture Overview

### Frontend
- React Native

### Backend
- Node.js / FastAPI

### AI Engine
- Rule-based + content-based + collaborative filtering

### Database
- PostgreSQL
- Redis
- S3

---

## 6. AI Logic

1. Filter (remove allergens & invalid meals)
2. Score (nutrition + preferences)
3. Rank (best matches)
4. Diversify (avoid repetition)

---

## 7. Constraints

- Build timeline: 3 months
- No medical claims
- Mobile-first performance

---

## 8. Success Metrics

- Day 7 retention ≥ 40%
- Day 30 retention ≥ 20%
- DAU/MAU ≥ 25%
- Meal adherence ≥ 35%
- Avg rating ≥ 3.8

---

## 9. Risks

- Cold start → rule-based fallback
- Low engagement → gamification
- Trust issues → explainable AI

---

## 10. Notes for Developers

- Ensure allergen safety at all times
- Keep response latency low
- Design for future ML upgrades
- Avoid hardcoding logic
