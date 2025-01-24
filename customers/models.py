from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False,
                                limit_choices_to={'department__name': 'коммерческий'},  # Ограничение выбора
                                verbose_name='Менеджер')

    def __str__(self):
        """
        Возвращает строковое представление объекта заказчика.
        Используется для отображения в админке.
        """
        return f"{self.name} ({self.code})"
