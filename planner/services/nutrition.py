"""Transparent adult nutrition estimates; no measurement data is persisted."""

import math


ACTIVITIES = {
    "sedentary": ("Mostly seated, little exercise", 1.2),
    "light": ("Light activity / exercise 1–3 days a week", 1.375),
    "moderate": ("Moderate activity / exercise 3–5 days a week", 1.55),
    "active": ("Very active / hard exercise 6–7 days a week", 1.725),
    "very_active": ("Physical job plus hard training", 1.9),
}


def number(values, key, label, minimum, maximum):
    try:
        value = float(values.get(key, ""))
    except (ValueError, TypeError):
        raise ValueError(f"Enter a valid {label}.") from None
    if not math.isfinite(value) or not minimum <= value <= maximum:
        raise ValueError(f"{label.capitalize()} must be between {minimum} and {maximum}.")
    return value


def macros(calories, weight, protein_factor):
    """Use 30% of energy for fat and allocate remaining energy to carbs."""
    protein = weight * protein_factor
    fat = calories * 0.30 / 9
    carbs = (calories - protein * 4 - fat * 9) / 4
    if carbs < 0:
        return None
    daily = {"calories": round(calories), "protein": round(protein),
             "carbs": round(carbs), "fat": round(fat)}
    return {"daily": daily, "weekly": {key: value * 7 for key, value in daily.items()}}


def calculate_plan(values):
    age = number(values, "age", "age (years)", 18, 100)
    weight = number(values, "weight", "weight (kg)", 30, 350)
    height = number(values, "height", "height (cm)", 120, 230)
    waist = number(values, "waist", "waist (cm)", 40, 250)
    neck = number(values, "neck", "neck (cm)", 20, 80)
    sex = values.get("sex")
    activity = values.get("activity")
    if sex not in ("male", "female"):
        raise ValueError("Choose a sex used by the estimation equations.")
    if activity not in ACTIVITIES:
        raise ValueError("Choose an activity level.")
    if waist <= neck:
        raise ValueError("Waist must be larger than neck. Check your measurements.")

    # Historical Navy circumference equations use inches, not centimeters.
    if sex == "male":
        body_fat = (86.010 * math.log10((waist - neck) / 2.54)
                    - 70.041 * math.log10(height / 2.54) + 36.76)
    else:
        hip = number(values, "hip", "hip (cm)", 40, 250)
        body_fat = (163.205 * math.log10((waist + hip - neck) / 2.54)
                    - 97.684 * math.log10(height / 2.54) - 78.387)
    if not 2 <= body_fat <= 65:
        raise ValueError("These measurements give a body-fat estimate outside this calculator's range (2–65%). Check the measuring instructions.")

    bmr = 10 * weight + 6.25 * height - 5 * age + (5 if sex == "male" else -161)
    maintenance = bmr * ACTIVITIES[activity][1]
    if bmr <= 0:
        raise ValueError("These measurements do not produce a valid calorie estimate.")
    bmi = weight / (height / 100) ** 2
    floor = 1500 if sex == "male" else 1200
    loss = []
    for rate in (0.25, 0.5, 0.75):
        calories = maintenance - rate * 7700 / 7
        reason = None
        if bmi < 18.5:
            reason = "Fat-loss targets are not shown for a BMI below 18.5. Seek an individual assessment."
        elif calories < floor:
            reason = f"Below this calculator's {floor:,} kcal/day screening limit. Choose a slower goal or seek individual advice."
        elif rate / weight > 0.01:
            reason = "Exceeds 1% of your body weight per week. Choose a slower goal."
        plan = macros(calories, weight, 2.0) if not reason else None
        if not plan and not reason:
            reason = "This calorie budget cannot accommodate the selected macro allocation."
        loss.append({"rate": rate, "plan": plan, "reason": reason})
    return {
        "body_fat": round(body_fat, 1), "bmr": round(bmr),
        "fat_mass": round(weight * body_fat / 100, 1),
        "lean_mass": round(weight * (1 - body_fat / 100), 1),
        "maintenance": macros(maintenance, weight, 1.6), "loss": loss,
        "gain": macros(maintenance * 1.10, weight, 1.8),
        "gain_rates": (0.25, 0.5, 0.76),
    }
