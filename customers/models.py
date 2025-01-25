from django.core.exceptions import ValidationError
from django.db import models
from users.models import CustomUser


class Customer(models.Model):
    """
    Модель для представления заказчиков.

    Атрибуты:
        name (CharField): Название заказчика.
                          Может быть пустым.
        city (CharField): Город заказчика.
                          Может быть пустым.
        code (CharField): Уникальный код заказчика.
                         Обязательно уникальное значение.
                         Может быть пустым.
        manager (ForeignKey): Связь с моделью CustomUser.
                            Означает, что у каждого заказчика есть менеджер.
                            Поле не может быть пустым.
                            Менеджер должен быть из коммерческого отдела.
    """
    name = models.CharField(max_length=255, verbose_name='Название', null=True, blank=True)
    city = models.CharField(max_length=255, verbose_name='Город', null=True, blank=True)
    code = models.CharField(max_length=10, unique=True, verbose_name='Код', null=True, blank=True)
    manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=False,
                                verbose_name='Менеджер')

    def __str__(self):
        """
        Возвращает строковое представление объекта заказчика.
        Используется для отображения в админке.
        """
        return f"{self.name} ({self.code})"

    def clean(self):
        """Валидация менеджера."""
        if self.manager and self.manager.department.name != 'коммерческий':
            raise ValidationError({'manager': 'Менеджер должен быть из коммерческого отдела.'})