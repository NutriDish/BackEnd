def handle_user_input(request):
    # Initialize default nutritional constraints
    nutritional_constraints = {
        "calories": {"min": 0, "max": 9999},
        "protein": {"min": 0, "max": 9999},
        "fat": {"min": 0, "max": 9999},
        "sodium": {"min": 0, "max": 9999},
    }
    # Update constraints if provided
    if "nutritional_constraints" in request:
        for nutrient, values in request["nutritional_constraints"].items():
            if nutrient in nutritional_constraints:
                nutritional_constraints[nutrient]["min"] = values.get("min", 0)
                nutritional_constraints[nutrient]["max"] = values.get("max", 9999)

    # Handle tags
    default_tags = {
        "breakfast": False, "lunch": False, "dinner": False,
        "snack": False, "dessert": False, "vegetarian": False,
        "vegan": False, "pescatarian": False, "paleo": False,
        "dairy free": False, "fat free": False, "peanut free": False,
        "soy free": False, "wheat/gluten-free": False, "low carb": False,
        "low cal": False, "low fat": False, "low sodium": False,
        "low sugar": False, "low cholesterol": False, "winter": False,
        "spring": False, "summer": False, "fall": False, "alcoholic": False,
        "non-alcoholic": False, "pork": False,
    }
    # Set absolute tags for weekly plan
    for tag in ["breakfast", "lunch", "dinner", "snack", "dessert"]:
        default_tags[tag] = True

    if "tags" in request:
        for tag, value in request["tags"].items():
            if tag in default_tags:
                default_tags[tag] = value

    return {
        "keywords": request.get("keywords", ""),
        "ingredients": request.get("ingredients", []),
        "nutritional_constraints": nutritional_constraints,
        "tags": default_tags,
    }