from rest_framework import serializers

from .models import Category, Subcategory

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = ('title', 'slug')

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('title', 'slug', 'subcategories')
