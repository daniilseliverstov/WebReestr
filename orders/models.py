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

    # Поля для материалов
    mdf = models.BooleanField(default=False, verbose_name='МДФ')
    fittings = models.BooleanField(default=False, verbose_name='Фурнитура')
    glass = models.BooleanField(default=False, verbose_name='Стекла')
    cnc = models.BooleanField(default=False, verbose_name='ЧПУ')
    ldsp_area = models.FloatField(blank=True, null=True, verbose_name='ЛДСП 16-25мм, АГТ (м²)')
    mdf_area = models.FloatField(blank=True, null=True, verbose_name='МДФ (м²)')
    edge_04 = models.FloatField(blank=True, null=True, verbose_name='Кромка 0,4мм (м/п)')
    edge_2 = models.FloatField(blank=True, null=True, verbose_name='Кромка 2мм (м/п)')
    edge_1 = models.FloatField(blank=True, null=True, verbose_name='Кромка 1мм (м/п)')
    total_area = models.FloatField(blank=True, null=True, verbose_name='Общая площадь (м²)')
    serial_area = models.FloatField(blank=True, null=True, verbose_name='Площадь серийной продукции (м²)')
    portal_area = models.FloatField(blank=True, null=True, verbose_name='Площадь каминных порталов (м²)')
    complaint_reason = models.TextField(blank=True, null=True, verbose_name='Причина рекламации')

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

