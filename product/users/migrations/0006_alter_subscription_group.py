# Generated by Django 4.2.10 on 2024-08-17 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_remove_group_subscription'),
        ('users', '0005_alter_balance_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='group',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='courses.group', verbose_name='Группа'),
        ),
    ]
