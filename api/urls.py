from django.urls import path
# from django.urls import include
# from rest_framework.routers import DefaultRouter
from .views import (ingredients, FavoritesView, SubscriptionView,
                    ShoppingListView)

# router_v1 = DefaultRouter()
# router_v1.register('favorites', FavoritesViewSet)

urlpatterns = [
    path('v1/ingredients/', ingredients),
    path('v1/favorites/', FavoritesView.as_view()),
    path('v1/favorites/<int:recipe_id>/', FavoritesView.as_view()),
    path('v1/subscriptions/', SubscriptionView.as_view()),
    path('v1/subscriptions/<int:author_id>/', SubscriptionView.as_view()),
    path('v1/purchases/', ShoppingListView.as_view()),
    path('v1/purchases/<int:recipe_id>/', ShoppingListView.as_view()),
    # path('v1/', include(router_v1.urls)),

]
