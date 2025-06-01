# your_app_name/models.py
from django.db import models

class SavedRecipe(models.Model):
        # We use IntegerField for recipe_id as it comes from the Spoonacular API
    recipe_id = models.IntegerField(unique=True, help_text="Unique ID from Spoonacular API")
    title = models.CharField(max_length=255)
    image = models.URLField(max_length=500, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
        # You could add fields for ingredients if you want to store them
        # For example, if you want to store them as a JSON string:
        # extended_ingredients_json = models.JSONField(blank=True, null=True)
        # Or as a TextField if you prefer to just save the original string:
        # extended_ingredients_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Saved Recipe"
        verbose_name_plural = "Saved Recipes"
        ordering = ['-id'] # Default ordering, newest first
    

    