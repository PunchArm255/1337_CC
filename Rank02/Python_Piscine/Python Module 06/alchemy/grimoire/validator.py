def validate_ingredients(ingredients: str) -> str:
    for ing in ["fire", "air", "water", "earth"]:
        if ing in ingredients.lower():
            return f"{ingredients} - VALID"
    else:
        return f"{ingredients} - INVALID"
