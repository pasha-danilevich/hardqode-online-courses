from django.db.models import Count, QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import Subscription, SubscriptionGroup
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created:
        course = instance.course
        groups_on_course = course.groups.all()

        groups_with_counts = groups_on_course.annotate(
            subscription_count=Count('subscriptions_group'))

        group = _find_element_with_min_subscription(groups_with_counts)

        SubscriptionGroup.objects.create(
            subscription=instance,
            group=group
        )


def _find_element_with_min_subscription(data: QuerySet[Group]) -> Group:
    """Возвращает элемент с наименьшим значением subscription_count из QuerySet групп."""
    return min(data, key=lambda x: x.subscription_count)  # type: ignore
