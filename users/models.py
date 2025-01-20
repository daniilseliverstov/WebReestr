from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    """Класс описания Отделов. Состоит только из названия"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Класс профилей пользователей"""
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь с User
    department = models.CharField(
        max_length=100,
        choices=[
            ('commercial', 'Коммерческий отдел'),
            ('technical', 'Технический отдел'),
            ('design', 'Конструкторский отдел'),
            ('supply', 'Отдел снабжения'),
        ],
        verbose_name='Отдел'
    )

    def __str__(self):
        return f'{self.user.username} ({self.department})'

