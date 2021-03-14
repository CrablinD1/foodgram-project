from django.urls import path

from .views import (FavoritesView, ShoppingListView, SubscriptionView,
                    ingredients)

urlpatterns = [
    path('v1/ingredients/', ingredients),
    path('v1/favorites/', FavoritesView.as_view()),
    path('v1/favorites/<int:recipe_id>/', FavoritesView.as_view()),
    path('v1/subscriptions/', SubscriptionView.as_view()),
    path('v1/subscriptions/<int:author_id>/', SubscriptionView.as_view()),
    path('v1/purchases/', ShoppingListView.as_view()),
    path('v1/purchases/<int:recipe_id>/', ShoppingListView.as_view()),

]
