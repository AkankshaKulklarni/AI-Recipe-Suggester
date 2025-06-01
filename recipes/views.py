import requests
from django.shortcuts import render

API_KEY = "caff8b577bb44a67a5df87f1d7c8a398"

def get_recipes_by_ingredients(ingredients):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients,
        "number": 3,
        "ranking": 1,
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else []

def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

def main(request):
    recipes = []
    if request.method == "POST":
        ingredients = request.POST.get("ingredients")
        basic_recipes = get_recipes_by_ingredients(ingredients)
        # print(basic_recipes)
        for r in basic_recipes:
            details = get_recipe_details(r['id'])
            if details:
                recipes.append(details)
    return render(request, "recipes/home.html", {"recipes": recipes})
