from rest_framework.permissions import BasePermission, SAFE_METHODS
from courses.models import Course
from users.models import CustomUser, Subscription

class InsufficientFundsError(Exception):
    """Исключение для недостатка средств."""
    pass

def make_payment(user: CustomUser, course: Course):
    user_balance = user.balance.amount
    course_price = course.worth

    if user_balance < course_price:
        # Выбрасываем исключение, если средств недостаточно
        raise InsufficientFundsError("У вас недостаточно средств для выполнения платежа.")
    
    # Списываем деньги
    user.balance.amount = user_balance - course_price 
    user.balance.save()


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        # TODO
        pass

    def has_object_permission(self, request, view, obj):
        # TODO
        pass


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
