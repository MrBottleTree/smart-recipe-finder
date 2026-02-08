from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True) 
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, null=True, blank=True)
    purchase_link = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ingredients'

    def __str__(self):
        return self.name
#a tag is for a recipe like vegan , veg , non veg , spicy , sweet
class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.tag_name


#  One-to-Many Relationships

class SearchHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    search_query = models.CharField(max_length=255)
    searched_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_history'

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_recipes') 
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    cuisine = models.CharField(max_length=100, null=True, blank=True)
    prep_time_mins = models.IntegerField(null=True, blank=True)
    calories = models.IntegerField(null=True)
    approval_status = models.CharField(max_length=50, default='pending')

    # This 'through' field does not let create a hidden many to many table
    ingredients = models.ManyToManyField(
        Ingredient, 
        through='RecipeIngredient',
        related_name='recipes'
    )
    
    tags = models.ManyToManyField(
        Tag, 
        through='RecipeTag',
        related_name='recipes'
    )

    class Meta:
        db_table = 'recipes'

    def __str__(self):
        return self.title


# --- Many-to-Many Relationships

class RecipeIngredient(models.Model):
    """
    Connects Recipe and Ingredient with Quantity/Unit data.
    """
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    #to add this extra data we used foreign key and not manyto many directly
    #### unit represents g / kg / 1tbsp and quantity is representing the number
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    notes = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'recipe_ingredients'
        unique_together = (('recipe', 'ingredient'),)

    def __str__(self):
        return f"{self.recipe.title} - {self.ingredient.name}"

class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'recipe_tags'
        unique_together = (('recipe', 'tag'),)

class UserPantry(models.Model):
    pantry_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pantry_items')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)

    class Meta:
        db_table = 'user_pantry'

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'