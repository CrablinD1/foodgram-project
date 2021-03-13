from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import RecipeForm
from .models import Recipe, Ingredient, RecipeIngredient, User
from .utils import get_ingredients


def index(request):
    recipe_list = Recipe.objects.order_by('-pub_date').all()
    paginator = Paginator(recipe_list, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator})


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    context = {'form': form}
    if request.method != 'POST':
        return render(request, 'recipes/new_recipe.html', context)
    else:
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, "Добавьте ингредиенты")
        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            for ing_title, amount in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=ing_title)
                recipe_ing = RecipeIngredient(
                    recipe=recipe, ingredient=ingredient, amount=amount
                )
                recipe_ing.save()
            return redirect("index")


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.author_recipes.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/profile.html',
                  {'author': author, 'page': page, 'paginator': paginator})


def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(author.author_recipes, pk=recipe_id)

    return render(request, 'recipes/single_page.html',
                  {'author': author, 'recipe': recipe})
