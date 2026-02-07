from django.contrib import admin
from .models import (
    User, 
    Ingredient, 
    Tag, 
    SearchHistory, 
    Recipe, 
    RecipeIngredient, 
    RecipeTag, 
    UserPantry, 
    Review
)

# Register your models here.
admin.site.register(User)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(SearchHistory)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
admin.site.register(UserPantry)
admin.site.register(Review)