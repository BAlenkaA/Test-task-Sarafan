from rest_framework import serializers

from .models import Category, Subcategory


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для подкатегорий продуктов.
    Возвращает информацию о подкатегории:
    - title (название подкатегории)
    - slug (уникальный идентификатор)
    - image (изображение подкатегории)
    """

    class Meta:
        model = Subcategory
        fields = ('title', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    """
    Сериализатор для категорий продуктов.
    Возвращает информацию о категории, включая подкатегории:
    - title (название категории)
    - slug (уникальный идентификатор)
    - image (изображение категории)
    - subcategories (список связанных подкатегорий)
    """

    class Meta:
        model = Category
        fields = ('title', 'slug', 'image', 'subcategories')
