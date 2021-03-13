from django.urls import path

from . import views

urlpatterns = [
    path('ingredients/', views.ingredients),
]
