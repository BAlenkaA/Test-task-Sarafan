from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для продуктов. Возвращает информацию о продукте:
    - title (название продукта)
    - slug (уникальный идентификатор продукта)
    - category (название категории)
    - subcategory (название подкатегории)
    - price (цена продукта)
    - images (список изображений с абсолютными URL-адресами)
    """
    category = serializers.CharField(source='category.title')
    subcategory = serializers.CharField(source='subcategory.title')
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'title',
            'slug',
            'category',
            'subcategory',
            'price',
            'images'
        )

    def get_images(self, obj):
        """
        Метод для получения списка изображений продукта.
        Возвращает абсолютные URL для маленького,
        среднего и большого изображения.

        Args:
            obj (Product): экземпляр продукта.

        Returns:
            list: список абсолютных URL-адресов для изображений продукта.
        """
        request = self.context.get('request')
        image_fields = ['image_small', 'image_medium', 'image_large']
        return [
            request.build_absolute_uri(getattr(obj, image_field).url)
            for image_field in image_fields
            if getattr(obj, image_field)
        ]
