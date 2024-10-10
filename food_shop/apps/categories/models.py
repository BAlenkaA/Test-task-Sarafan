from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug-имя категории'
    )
    image = models.ImageField(
        upload_to='category_images/',
        verbose_name='Изображение'
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
        upload_to='subcategory_images/',
        verbose_name='Изображение'
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
