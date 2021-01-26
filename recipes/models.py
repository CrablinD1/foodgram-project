from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Ingredients(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    dimension = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes_author')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipe/', blank=True, null=True)
    description = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredient')
    tag = models.TextField()
    cooking_time = models.IntegerField()

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE,
                                   related_name='recipes')
    amount = models.IntegerField()