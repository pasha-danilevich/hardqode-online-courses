import time
from django.core.management.base import BaseCommand
from faker import Faker
from courses.models import Course, Lesson, Group
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Generate random data for Course, Lesson, and Group models'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('In progress...'))
        
        start_time = self.start_recording_time()
        
        # Генерация случайных данных
        self.generate_random_data()
        
        end_time = self.end_recording_time(start_time)
        
        self.stdout.write(self.style.SUCCESS(f'Data generation completed in {end_time:.2f} seconds'))

    def start_recording_time(self):
        """Запускает таймер и возвращает текущее время."""
        return time.time()
    
    def end_recording_time(self, start_time):
        """Завершает таймер и возвращает разницу во времени."""
        end_time = time.time()
        return end_time - start_time
    
    def generate_random_data(self):
        """Генерация случайных курсов, уроков и групп."""
        fake = Faker()
        
        # Генерация случайных курсов
        for _ in range(10):  
            # Генерация "aware" datetime
            naive_datetime = fake.date_time_this_year()
            aware_datetime = timezone.make_aware(naive_datetime)

            course = Course.objects.create(
                author=fake.name(),
                title=fake.sentence(nb_words=6),
                start_date=aware_datetime,  # Используем "aware" datetime
                worth=round(random.uniform(100, 500), 2),  # Случайная стоимость от 100 до 500
                available=random.choice([True, False])  # Случайная доступность
            )
            self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))

            # Генерация случайных уроков для каждого курса
            for _ in range(random.randint(1, 5)):
                Lesson.objects.create(
                    title=fake.sentence(nb_words=4),
                    link=fake.url(),
                    course=course
                )

            # Генерация 10 групп для каждого курса
            for _ in range(10):
                Group.objects.create(
                    title=fake.sentence(nb_words=3),
                    course=course
                )