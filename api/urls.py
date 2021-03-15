from django.urls import include, path

from .views import (FavoritesView, ShoppingListView, SubscriptionView,
                    ingredients)

v1_urlpatterns = [
    path('ingredients/', ingredients, name='ingredients'),
    path('favorites/', FavoritesView.as_view(), name='add_favorites'),
    path('favorites/<int:recipe_id>/', FavoritesView.as_view(),
         name='delete_favorites'),
    path('subscriptions/', SubscriptionView.as_view(), name='add_follow'),
    path('subscriptions/<int:author_id>/', SubscriptionView.as_view(),
         name='delete follow'),
    path('purchases/', ShoppingListView.as_view(), name='add_purchases'),
    path('purchases/<int:recipe_id>/', ShoppingListView.as_view(),
         name='delete_purchases'),
]

urlpatterns = [
    path("v1/", include(v1_urlpatterns)),
]
