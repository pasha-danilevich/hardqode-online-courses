from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, QuerySet
from rest_framework import serializers
from django.db.models import Prefetch

from courses.models import Course, Group, Lesson
from users.models import Subscription, SubscriptionGroup

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    # TODO Доп. задание

    class Meta:
        model = Group


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj: Course) -> int:
        """Количество уроков в курсе."""
        return obj.lessons.count()
        
        

    def get_students_count(self, obj: Course) -> int:
        """Общее количество студентов на курсе."""
        return obj.subscriptions.count()
    
    def _get_sum_subscription(self, groups: QuerySet[Group]) -> int:
        """Возвращает сумму учеников в группах"""
        return sum(group.subscriptions_count for group in groups)  # type: ignore

    def get_groups_filled_percent(self, obj: Course) -> float:
        """Средний процент заполненности групп, если максимум 30 чел."""
    
        groups = obj.groups.annotate(
            subscriptions_count=Count('subscriptions_group')
        ).prefetch_related('subscriptions_group')
        
        sum_subscription = self._get_sum_subscription(groups)
        
        max_capacity = 30
        total_groups = len(groups)
        
        # Вычисляем средний процент заполненности
        average_filled_percentage = (sum_subscription / (total_groups * max_capacity) * 100) if total_groups > 0 else 0
        
        return round(average_filled_percentage, 1)
    
    


    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        # TODO Доп. задание

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'worth',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
