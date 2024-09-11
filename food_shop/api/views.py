from django.db.models import F, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Product, ShoppigCart
from .serializers import (CategorySerializer, ListShopingCartSerializer,
                          ProductSerializer)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра категорий товаров.

    Методы:
    - list: Возвращает список всех категорий.
    - retrieve: Возвращает детали определенной категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра продуктов.

    Методы:
    - list: Возвращает список всех продуктов.
    - retrieve: Возвращает детали определенного продукта.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShopingCartViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления корзиной покупок пользователя.

    Доступные методы:
    - create: Добавление товара в корзину.
    - update: Обновление количества товара в корзине.
    - destroy: Удаление товара из корзины.
    - get_cart_summary: Получение общей информации о корзине
    (количество товаров и общая стоимость).
    - clear_cart: Полная очистка корзины.
    """
    serializer_class = ListShopingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает корзину текущего пользователя.
        """
        return ShoppigCart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Добавляет товар в корзину или обновляет количество,
        если товар уже в корзине.

        Параметры запроса:
        - product (int): ID товара.
        - amount (int): Количество (по умолчанию 1).

        Ответ:
        - Возвращает детали обновленного или созданного элемента корзины.
        """
        user = request.user
        product_id = request.data.get('product')
        amount = request.data.get('amount', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Продукт не найден.'},
                            status=status.HTTP_404_NOT_FOUND)

        cart_item, created = ShoppigCart.objects.get_or_create(
            user=user, product=product, defaults={'amount': amount})

        if not created:
            cart_item.amount += int(amount)
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Обновляет количество товара в корзине.

        Параметры запроса:
        - product (int): ID товара.
        - amount (int): Новое количество.

        Ответ:
        - Возвращает обновленную информацию о товаре в корзине.
        """
        user = request.user
        product_id = request.data.get('product')
        amount = request.data.get('amount')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Продукт не найден.'},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = ShoppigCart.objects.get(user=user, product=product)
        except ShoppigCart.DoesNotExist:
            return Response({'detail': 'Продукт не в корзине.'},
                            status=status.HTTP_404_NOT_FOUND)

        cart_item.amount = int(amount)
        cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Удаляет товар из корзины.

        Параметры URL:
        - pk (int): ID товара.

        Ответ:
        - Возвращает статус удаления товара.
        """
        user = request.user
        product_id = kwargs.get('pk')
        user = request.user
        product_id = kwargs.get('pk')

        try:
            cart_item = ShoppigCart.objects.get(
                user=user, product_id=product_id)
            cart_item.delete()
            return Response({'detail': 'Продукт удален из корзины.'},
                            status=status.HTTP_204_NO_CONTENT)
        except ShoppigCart.DoesNotExist:
            return Response({'detail': 'Продукт не найден в корзине.'},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='summary')
    def get_cart_summary(self, request):
        """
        Возвращает информацию о корзине:
        общее количество товаров и общая стоимость.

        Ответ:
        - total_products (int): Общее количество товаров.
        - total_product_price (decimal): Общая стоимость товаров.
        - products (list): Список товаров в корзине.
        """
        user = request.user
        products = ShoppigCart.objects.filter(user=user)

        total_products = products.aggregate(
            total_amount=Sum('amount'))['total_amount'] or 0
        total_price = products.aggregate(
            total_price=Sum(
                F('amount') * F('product__price')))['total_price'] or 0

        serializer = self.get_serializer(products, many=True)
        return Response({
            'total_products': total_products,
            'total_product_price': total_price,
            'products': serializer.data
        })

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        """
        Полностью очищает корзину текущего пользователя.

        Ответ:
        - Возвращает статус успешного удаления всех товаров из корзины.
        """
        user = request.user
        ShoppigCart.objects.filter(user=user).delete()
        return Response({'detail': 'Корзина полностью очищена.'},
                        status=status.HTTP_204_NO_CONTENT)
