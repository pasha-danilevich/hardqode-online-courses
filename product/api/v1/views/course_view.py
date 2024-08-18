from typing import cast
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course, Group, Lesson
from .services import get_group_with_fewest_subscriptions
from users.models import Subscription, SubscriptionGroup
from django.db.models import Prefetch
from users.models import CustomUser


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


# GET /api/v1/courses/: Получить список всех курсов.
# POST /api/v1/courses/: Создать новый курс.
# GET /api/v1/courses/{id}/: Получить информацию о конкретном курсе.
# PUT /api/v1/courses/{id}/: Обновить информацию о конкретном курсе.
# DELETE /api/v1/courses/{id}/: Удалить курс.
# POST /api/v1/courses/{id}/pay/: Купить доступ к курсу (подписка на курс).

class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.prefetch_related(
        Prefetch(
            'lessons', 
            queryset=Lesson.objects.all()
        )
    ).all()
    
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""
        user = cast(CustomUser, request.user)  
        user_balance = user.balance.amount

        try:
            course = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
            
        course_price = course.worth 
        
        if user_balance >= course_price:
            
            ### надо обернуть в atomic
            # тут списать деньги
                
            obj, created = Subscription.objects.get_or_create(
                user=user,
                course=course,
            )
            
            if not created:
                return Response(
                    data='У вас уже есть данный курс',
                    status=status.HTTP_400_BAD_REQUEST
                )  
            
        else:
            return Response(
                data='У вас недостаточно средств',
                status=status.HTTP_402_PAYMENT_REQUIRED
            )   
        
        data = f'{user.pk}, {pk}, {course_price}, {user_balance}'
        
        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )
