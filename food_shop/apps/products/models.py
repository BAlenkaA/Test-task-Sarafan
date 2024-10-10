from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.categories.models import Category, Subcategory


class Product(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Наименование товара'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug-имя товара'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    image_small = models.ImageField(
        upload_to='product_images/small',
        verbose_name='маленькое изображение',
        blank=True,
        null=True,
    )
    image_medium = models.ImageField(
        upload_to='product_images/medium',
        verbose_name='среднее изображение',
    )
    image_large = models.ImageField(
        upload_to='product_images/large',
        verbose_name='большое изображение',
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='цена товара',
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title
