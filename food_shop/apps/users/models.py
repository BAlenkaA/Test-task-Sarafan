from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
