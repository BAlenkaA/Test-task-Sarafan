from rest_framework import serializers

from apps.products.serializers import ProductSerializer

from .models import ShoppigCart


class ListShopingCartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для корзины покупок.
    Возвращает информацию о продукте в корзине:
    - product (сериализованный продукт)
    - amount (количество данного продукта в корзине)
    - total_price (общая стоимость товара в корзине)
    """
    total_price = serializers.SerializerMethodField()
    product = ProductSerializer()

    class Meta:
        model = ShoppigCart
        fields = ('product', 'amount', 'total_price')

    def get_total_price(self, obj):
        """
        Метод для получения общей стоимости товара в корзине.

        Args:
            obj (ShoppigCart): экземпляр элемента корзины.

        Returns:
            decimal: общая стоимость продукта в корзине.
        """
        return obj.product.price * obj.amount
