import pymorphy2
from django import template
from django.conf import settings
from recipes.models import FavoriteRecipe, Subscription, Tag

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def is_favorite(recipe, user):
    return FavoriteRecipe.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def all_tags(value):
    return Tag.objects.all()


@register.filter
def get_active_tags(value):
    return value.getlist('tag')


@register.filter
def change_tag_link(request, tag):
    copy = request.GET.copy()
    tag_link = copy.getlist('tag')
    if tag.slug in tag_link:
        tag_link.remove(tag.slug)
        copy.setlist('tag', tag_link)
    else:
        copy.appendlist('tag', tag.slug)
    return copy.urlencode()


@register.filter
def is_subscribe(author, user):
    return Subscription.objects.filter(author=author, user=user).exists()


@register.filter
def subtract(num1, num2):
    return num1 - num2


@register.filter
def word_form(word, number):
    morph = pymorphy2.MorphAnalyzer()
    default_word = morph.parse(word)[0]
    changed_word = default_word.make_agree_with_number(number).word
    return changed_word


@register.filter
def in_shopping_list(request, recipe_id):
    try:
        return str(recipe_id) in request.session[settings.PURCHASE_SESSION_ID]
    except KeyError:
        return False


@register.filter
def shopping_count(request):
    try:
        return len(request.session[settings.PURCHASE_SESSION_ID])
    except KeyError:
        return 0
