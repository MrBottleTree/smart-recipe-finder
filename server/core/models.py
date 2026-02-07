from django.db import models
from django.conf import settings


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)
    purchase_link = models.TextField(blank=True)
    image_url = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag_name


class Recipe(models.Model):
    APPROVAL_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes"
    )

    title = models.CharField(max_length=255)
    instructions = models.TextField()
    cuisine = models.CharField(max_length=100)
    prep_time_mins = models.IntegerField()
    calories = models.IntegerField()

    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default="pending"
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes"
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        blank=True
    )

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    quantity_required = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50)
    notes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.ingredient.name} - {self.recipe.title}"


class UserPantry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pantry_items"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user} - {self.ingredient.name}"


class Review(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.recipe.title}"


class SearchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="search_history"
    )
    search_query = models.CharField(max_length=255)
    searched_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.search_query
