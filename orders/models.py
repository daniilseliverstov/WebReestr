from django.core.exceptions import ValidationError
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


class Customer(models.Model):
    """Класс описания Заказчиков."""
    name = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    manager = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=False,
                                limit_choices_to={'department': 'commercial'},  # Ограничение выбора
                                verbose_name='Менеджер')

    def __str__(self):
        return f"{self.name} ({self.code})"

    def clean(self):
        """Проверяем, что менеджер из коммерческого отдела."""
        if self.manager and self.manager.department != 'commercial':
            raise ValidationError({'manager': 'Менеджер должен быть из коммерческого отдела.'})


class Orders(models.Model):
    """Класс заказов, сложно...."""
    pass
