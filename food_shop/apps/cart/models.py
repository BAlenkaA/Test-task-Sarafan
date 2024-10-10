from django.db import models

from apps.products.models import Product
from apps.users.models import CustomUser


class ShoppigCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        db_index=False
    )
    amount = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'
        unique_together = ('user', 'product')
