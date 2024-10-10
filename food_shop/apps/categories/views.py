from rest_framework import viewsets

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра категорий товаров.

    Методы:
    - list: Возвращает список всех категорий.
    - retrieve: Возвращает детали определенной категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
