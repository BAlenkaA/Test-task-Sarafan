from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class CustomUser(AbstractUser):

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug-имя категории'
    )
    image = models.ImageField(
        upload_to='api/category_images/',
        verbose_name='Изображение',
        blank=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug-имя подкатегории'
    )
    image = models.ImageField(
        upload_to='api/subcategory_images/',
        verbose_name='Изображение',
        blank=True
    )
    parent_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Родительская категория'
    )

    class Meta:
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Наименование продукта'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug-имя продукта'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    image_small = models.ImageField(
        upload_to='api/product_images/small',
        blank=True
    )
    image_medium = models.ImageField(
        upload_to='api/product_images/medium',
        blank=True
    )
    image_large = models.ImageField(
        upload_to='api/product_images/large',
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title


class ShoppigCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        db_index=False
    )
    amount = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'
        unique_together = ('user', 'product')
