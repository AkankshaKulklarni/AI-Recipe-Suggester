# your_app_name/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('save-recipe/', views.save_recipe, name='save_recipe'),
    path('saved-recipes/', views.saved_recipes_list, name='saved_recipes'),
    # New URL for unsaving recipes
    path('unsave-recipe/', views.unsave_recipe, name='unsave_recipe'),
]
