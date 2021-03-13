from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=255, verbose_name='ingredient title')
    dimension = models.CharField(max_length=64,
                                 verbose_name='ingredient dimension')

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.dimension}'


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    color = models.SlugField(verbose_name='tag color')

    def __str__(self):
        return f'{self.title}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_recipes')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipe/', blank=True,
                              null=True)
    description = models.TextField(verbose_name='recipe description')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         blank=True)  # related
    tags = models.ManyToManyField(Tag, related_name='recipe_tag', blank=True)
    cooking_time = models.PositiveIntegerField()
    pub_date = models.DateTimeField(verbose_name='date published',
                                    auto_now_add=True,
                                    db_index=True)

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.author}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='ingredient_amount')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_amount')
    amount = models.IntegerField()
