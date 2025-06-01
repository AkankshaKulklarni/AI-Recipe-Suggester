import requests
from django.shortcuts import render, redirect
from django.db.models import Q # Import Q object for complex lookups
from .models import SavedRecipe

API_KEY = "caff8b577bb44a67a5df87f1d7c8a398"

def get_recipes_by_ingredients(ingredients):
    """
    Fetches a list of recipes from the Spoonacular API based on provided ingredients.
    """
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients,
        "number": 3, # Requesting 3 recipes
        "ranking": 1, # Maximize used ingredients (1 for highest ranking)
        "apiKey": API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recipes by ingredients: {e}")
        return []

def get_recipe_details(recipe_id):
    """
    Fetches detailed information for a specific recipe from the Spoonacular API.
    """
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recipe details for ID {recipe_id}: {e}")
        return None

def home_view(request):
    """
    Handles the main recipe search page.
    Fetches recipes based on user-provided ingredients via POST request.
    """
    recipes = []
    if request.method == "POST":
        ingredients = request.POST.get("ingredients")
        if ingredients:
            basic_recipes = get_recipes_by_ingredients(ingredients)
            for r in basic_recipes:
                details = get_recipe_details(r['id'])
                if details:
                    details['extendedIngredients'] = details.get('extendedIngredients', [])
                    details['instructions'] = details.get('instructions', 'No instructions available.')
                    recipes.append(details)
    return render(request, "recipes/home.html", {"recipes": recipes})

def save_recipe(request):
    """
    Handles saving a recipe to the database.
    Expects a POST request with recipe details.
    """
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        title = request.POST.get('recipe_title')
        image = request.POST.get('recipe_image')
        instructions = request.POST.get('recipe_instructions')

        if instructions is None:
            instructions_str = ''
        else:
            instructions_str = str(instructions)

        if not SavedRecipe.objects.filter(recipe_id=recipe_id).exists():
            try:
                SavedRecipe.objects.create(
                    recipe_id=recipe_id,
                    title=title,
                    image=image,
                    instructions=instructions_str,
                )
                print(f"Recipe '{title}' (ID: {recipe_id}) saved successfully.")
            except Exception as e:
                print(f"Error saving recipe '{title}' (ID: {recipe_id}): {e}")
        else:
            print(f"Recipe '{title}' (ID: {recipe_id}) is already saved.")

        # --- MODIFICATION START ---
        # Instead of redirecting, render the home view again with a success message
        # or simply return a response that indicates success.
        # For simplicity, we'll redirect back to the home page without any specific message.
        # If you need to display a message, you'd typically use Django's messages framework.
        return redirect('home_view')
        # --- MODIFICATION END ---

    return redirect('home_view')

def saved_recipes_list(request):
    """
    Displays a list of all recipes saved by the user, with search functionality.
    """
    saved_recipes = SavedRecipe.objects.all().order_by('-id') # Start with all recipes

    # Check for a search query in the GET request
    query = request.GET.get('q')
    if query:
        # Filter saved recipes by title (case-insensitive contains)
        # You can add more fields to search, e.g., | Q(ingredients_field__icontains=query)
        saved_recipes = saved_recipes.filter(
            Q(title__icontains=query)
            # Add other fields if you save them and want to search by them
            # | Q(instructions__icontains=query)
        )

    context = {'saved_recipes': saved_recipes, 'query': query} # Pass the query back to the template
    return render(request, 'recipes/saved_recipes.html', context)

def unsave_recipe(request):
    """
    Handles unsaving (deleting) a recipe from the database.
    Expects a POST request with the recipe_id.
    """
    if request.method == 'POST':
        recipe_id_to_delete = request.POST.get('recipe_id')
        try:
            saved_recipe = SavedRecipe.objects.get(recipe_id=recipe_id_to_delete)
            saved_recipe.delete()
            print(f"Recipe (ID: {recipe_id_to_delete}) unsaved successfully.")
        except SavedRecipe.DoesNotExist:
            print(f"Recipe (ID: {recipe_id_to_delete}) not found in saved recipes.")
        except Exception as e:
            print(f"Error unsaving recipe (ID: {recipe_id_to_delete}): {e}")

    return redirect('saved_recipes') # Always redirect back to the saved recipes list