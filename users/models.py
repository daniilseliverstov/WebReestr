from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
    """
    Модель для представления отделов компании.

    Атрибуты:
        name (CharField): Название отдела (например, "Коммерческий", "Технический").
                         Уникальное значение.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Название отдела')

    def __str__(self):
        """
        Возвращает строковое представление объекта отдела.
        Используется для отображения в админке.
        """
        return self.name


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя, наследуемая от AbstractUser Django.
    Добавляет связь с отделом.

    Атрибуты:
        department (ForeignKey): Связь с моделью Department.
                              Позволяет пользователю быть связанным с определенным отделом.
                              Поле может быть пустым.
    """
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,
                                   null=True, blank=True, verbose_name='Отдел')

    def __str__(self):
        """
        Возвращает строковое представление объекта пользователя.
        Используется для отображения в админке.
        """
        return self.username
