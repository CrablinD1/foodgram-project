import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from foodgram.settings import OBJECT_PER_PAGE

from .forms import RecipeForm
from .models import (FavoriteRecipe, Recipe, RecipeIngredient, Subscription,
                     User)

logging.basicConfig(filename='log.txt', level=logging.INFO)


def index(request):
    tags = request.GET.getlist('tag')
    recipe_list = Recipe.objects.tag_filter(tags)
    paginator = Paginator(recipe_list, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator})


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      initial={"request": request}, )
    context = {'form': form}
    if request.method != 'POST':
        return render(request, 'recipes/new_recipe.html', context)
    else:
        if form.is_valid():
            form.save()
            return redirect('index')


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    if recipe.author != request.user:
        return redirect('recipe_view', username, recipe_id)
    else:
        form = RecipeForm(request.POST or None, files=request.FILES or None,
                          initial={"request": request},
                          instance=recipe)
        if request.method == 'POST':
            if form.is_valid():
                RecipeIngredient.objects.filter(recipe=recipe).delete()
                form.save()
                return redirect('recipe_view', username, recipe_id)
        return render(request, 'recipes/new_recipe.html',
                      {'form': form, 'recipe': recipe})


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    if request.user != request.user:
        return redirect('recipe_view', username, recipe_id)
    recipe.delete()
    return redirect('index')


def profile(request, username):
    tags = request.GET.getlist('tag')
    author = get_object_or_404(User, username=username)
    post_list = Recipe.objects.tag_filter(tags).filter(author=author)
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/profile.html',
                  {'author': author, 'page': page, 'paginator': paginator})


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    return render(request, 'recipes/single_page.html',
                  {'author': recipe.author, 'recipe': recipe})


@login_required
def favorite_recipe(request):
    tags = request.GET.getlist('tag')
    favorite_list = FavoriteRecipe.objects.favorite_recipe(request.user, tags)
    paginator = Paginator(favorite_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if not page:
        return render(request, 'recipes/custom_page.html')
    return render(request, 'recipes/favorite.html',
                  {'page': page, 'paginator': paginator})


@login_required
def subscriptions_index(request):
    subscriptions_list = Subscription.objects.subscriptions(user=request.user)
    paginator = Paginator(subscriptions_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if not page:
        return render(request, 'recipes/custom_page.html')
    return render(request, 'recipes/subscription.html',
                  {'page': page, 'paginator': paginator})


def shopping_list(request):
    try:
        recipes = Recipe.objects.filter(
            pk__in=request.session[settings.PURCHASE_SESSION_ID])
    except Exception as e:
        logging.error(str(e))
        return render(request, 'recipes/custom_page.html')
    if not recipes:
        return render(request, 'recipes/custom_page.html')
    return render(request, 'recipes/shopping_list.html', {'recipes': recipes})


def delete_purchase(request, recipe_id):
    try:
        request.session[settings.PURCHASE_SESSION_ID].remove(str(recipe_id))
        request.session.save()
    except Exception as e:
        logging.error(str(e))
    return redirect('shopping_list')


def save_shopping_list(request):
    try:
        recipes = Recipe.objects.filter(
            pk__in=request.session[settings.PURCHASE_SESSION_ID])
        ingredients = recipes.values(
            'ingredients__title', 'ingredients__dimension').annotate(
            total_amount=Sum('recipe_amounts__amount'))
        filename = 'shopping_list.txt'
        content = ''
        for ingredient in ingredients:
            string = (f'{ingredient["ingredients__title"]} '
                      f'({ingredient["ingredients__dimension"]}) - '
                      f'{ingredient["total_amount"]}')
            content += string + '\n'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            filename)
        return response
    except Exception as e:
        logging.error(str(e))
        return render(request, 'recipes/custom_page.html')
