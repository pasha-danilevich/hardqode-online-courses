from django.db import models
from configuration import settings
from users.models import Subscription, SubscriptionGroup


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    worth = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость'
    )
    available = models.BooleanField(
        default=True, 
        verbose_name='Доступен'
    )

    lessons: 'models.QuerySet[Lesson]'
    subscriptions: 'models.QuerySet[Subscription]'
    groups: 'models.QuerySet[Group]'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка на видео',
    )
    course = models.ForeignKey(
        'courses.Course',
        related_name='lessons',
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )
    
    course: 'models.ForeignKey[Course]'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""
    
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    course = models.ForeignKey(
        'courses.Course',
        related_name='groups',
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )
    
    subscriptions_group: 'models.QuerySet[SubscriptionGroup]'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)
