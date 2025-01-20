from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

from materials.models import Materials
from users.models import Profile
from customers.models import Customer


class Orders(models.Model):
    """Класс заказов, сложно...."""
    STATUS_CHOICES = [
        ('accepted', 'Принят'),
        ('in_progress', 'В работе'),
        ('clarification', 'Уточнение'),
        ('documents', 'Документы'),
        ('postponed', 'Перенос'),
        ('completed', 'Готово'),
    ]

    # Основные поля заказа
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name='Заказчик')
    order_number = models.CharField(max_length=50, unique=True, verbose_name='Номер заказа')
    month = models.IntegerField(verbose_name='Месяц заказа')
    week = models.IntegerField(verbose_name='Производственная неделя')
    manager = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='managed_orders',
                                verbose_name='Менеджер')
    weight = models.FloatField(blank=True, null=True, verbose_name='Масса')
    package_count = models.IntegerField(blank=True, null=True, verbose_name='Количество упаковок')
    start_date = models.DateField(blank=True, null=True, verbose_name='Дата начала обработки')
    assigned_to = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_orders', verbose_name='Исполнитель')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='accepted', verbose_name='Статус заказа')

    # Метод для отображения заказа в админке
    def __str__(self):
        return f"{self.order_number} ({self.get_status_display()})"

    # Валидация заказа
    def clean(self):
        # Проверка, что менеджер из коммерческого отдела
        if self.manager and self.manager.department != 'commercial':
            raise ValidationError({'manager': 'Менеджер должен быть из коммерческого отдела.'})

        # Проверка, что исполнитель из технического или конструкторского отдела
        if self.assigned_to and self.assigned_to.department not in ['technical', 'design']:
            raise ValidationError(
                {'assigned_to': 'Исполнитель должен быть из технического или конструкторского отдела.'})

    def get_status_display(self):
        """Надо сделать!"""
        pass


class AdditionalOrder(models.Model):
    TYPE_CHOICES = [
        ('supplement', 'ДОП'),
        ('complete', 'ДОД'),
        ('Claim', 'РЕК')
    ]
    parent_order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    type_ = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Claim', verbose_name='Статус заказа')
    materials = models.OneToOneField(Materials, on_delete=models.CASCADE)
    complaint_reason = models.TextField(blank=True, null=True, verbose_name='Причина рекламации')
