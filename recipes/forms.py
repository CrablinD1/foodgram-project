from django.forms import (CheckboxSelectMultiple, ModelForm,
                          ModelMultipleChoiceField)
from django.shortcuts import get_object_or_404

from .models import Ingredient, Recipe, RecipeIngredient, Tag
from .utils import get_ingredients


class RecipeForm(ModelForm):
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                    widget=CheckboxSelectMultiple(
                                        attrs={'class': 'tags__checkbox'}),
                                    required=False
                                    )

    def save(self, commit=True):
        request = self.initial["request"]
        recipe = super().save(commit=False)
        recipe.author = request.user
        recipe.save()
        self.save_m2m()
        ingredients = get_ingredients(request)
        for title, amount in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            recipe_ing = RecipeIngredient(recipe=recipe,
                                          ingredient=ingredient,
                                          amount=amount)
            recipe_ing.save()

    class Meta:
        model = Recipe
        fields = ('title', 'cooking_time', 'description', 'image',
                  'tags', 'ingredients')
