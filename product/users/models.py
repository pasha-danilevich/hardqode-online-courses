from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

from configuration import settings
from courses.models import *

class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password'
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='balance',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('1000.00'),
        verbose_name='Баланс'
    )
    
    user: 'models.OneToOneField[CustomUser]'
    subscriptions: 'models.QuerySet[Subscription]'

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    def __str__(self):
        return f"Баланс пользователя {self.user.username}: {self.amount} бонусов"

    def save(self, *args, **kwargs):

        if self.amount < 0:
            raise ValidationError("Баланс не может быть ниже 0.")
        super().save(*args, **kwargs)


class Subscription(models.Model):
    """
    Модель подписки пользователя на курс.

    Атрибуты:
        user (ForeignKey): Пользователь, связанный с подпиской.
        course (ForeignKey): Курс, на который оформлена подписка.
        subscription_date (DateTimeField): Дата и время создания подписки.
        group (OneToOneField): Группа, связанная с подпиской.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Связываем с кастомной моделью пользователя
        related_name='subscriptions',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        'courses.Course',
        related_name='subscriptions',
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )
    subscription_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подписки'
    )
    group = models.OneToOneField(
        'courses.Group',
        related_name='subscriptions',
        on_delete=models.CASCADE,
        verbose_name='Группа'
    )
    
    user: 'models.ForeignKey[CustomUser]'
    course: 'models.ForeignKey[Course]'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-subscription_date',)  # Сортировка по дате подписки

    def __str__(self):
        return f"{self.user.username} подписан на {self.course.title}"
