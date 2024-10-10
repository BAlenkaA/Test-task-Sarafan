from rest_framework import viewsets

from apps.products.models import Product
from apps.products.serializers import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра продуктов.

    Методы:
    - list: Возвращает список всех продуктов.
    - retrieve: Возвращает детали определенного продукта.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
