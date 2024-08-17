# Generated by Django 4.2.10 on 2024-08-17 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0003_alter_lesson_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='courses.course', verbose_name='Курс'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='course_groups', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
    ]
