from django.http import JsonResponse
from rest_framework.decorators import api_view

from recipes.models import Ingredient

from .serializers import IngredientSerializer


@api_view(['GET'])
def ingredients(request):
    query = request.GET.get('query', '')
    data = Ingredient.objects.filter(title__contains=query).all()
    serializer = IngredientSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)
