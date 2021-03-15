from django.urls import path

from .views import (FavoritesView, ShoppingListView, SubscriptionView,
                    ingredients)

urlpatterns = [
    path('ingredients/', ingredients),
    path('favorites/', FavoritesView.as_view()),
    path('favorites/<int:recipe_id>/', FavoritesView.as_view()),
    path('subscriptions/', SubscriptionView.as_view()),
    path('subscriptions/<int:author_id>/', SubscriptionView.as_view()),
    path('purchases/', ShoppingListView.as_view()),
    path('purchases/<int:recipe_id>/', ShoppingListView.as_view()),
]
