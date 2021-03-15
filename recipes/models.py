from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .managers import FavoriteRecipeManager, RecipeManager

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=255, verbose_name='ingredient title')
    dimension = models.CharField(max_length=64,
                                 verbose_name='ingredient dimension')

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.dimension}'


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='tag title')
    slug = models.SlugField(max_length=50, verbose_name='tag slug',
                            unique=True)
    color = models.SlugField(verbose_name='tag color')

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __str__(self):
        return f'{self.title}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_recipes')
    title = models.CharField(max_length=255, verbose_name='recipe title')
    image = models.ImageField(upload_to='recipe/', blank=True, null=True,
                              verbose_name='recipe image')
    description = models.TextField(verbose_name='recipe description')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         blank=True)
    tags = models.ManyToManyField(Tag, related_name='recipe_tag', blank=True)
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='recipe cooking time')
    pub_date = models.DateTimeField(verbose_name='date published',
                                    auto_now_add=True,
                                    db_index=True)

    objects = RecipeManager()

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.author}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredient_amount')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_amount')
    amount = models.IntegerField()

    class Meta:
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipes Ingredients'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorite_recipes')

    objects = FavoriteRecipeManager()

    def __str__(self):
        return f'{self.pk} - {self.user} - {self.recipe}'


class SubscriptionManager(models.Manager):

    @staticmethod
    def subscriptions(user):
        sub_obj = Subscription.objects.filter(user=user)
        author_id = sub_obj.values_list('author', flat=True)
        subscriptions_list = User.objects.filter(pk__in=author_id)
        return subscriptions_list


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    objects = SubscriptionManager()

    def __str__(self):
        return f'{self.pk} - {self.user} - {self.author}'
