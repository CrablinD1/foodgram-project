def get_ingredients(request):
    ingredients = {}
    for key, title in request.POST.items():
        if 'nameIngredient' in key:
            elem = key.split("_")
            ingredients[title] = int(
                request.POST[f'valueIngredient_{elem[1]}'])
    return ingredients
