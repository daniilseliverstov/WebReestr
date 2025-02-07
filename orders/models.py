from django.core.exceptions import ValidationError
from django.db import models
from users.models import CustomUser
from customers.models import Customer
from datetime import datetime


class Order(models.Model):
    """
    Модель для представления заказов.
    """

    STATUS_CHOICES = [
        ('accepted', 'Принят'),
        ('in_progress', 'В работе'),
        ('clarification', 'Уточнение'),
        ('documents', 'Документы'),
        ('postponed', 'Перенос'),
        ('completed', 'Готово'),
    ]

    ORDER_TYPES = [
        ('Н', '(Н) Нестандартные заказы'),
        ('К', '(К) Нестандартные заказы кухни'),
        ('ЛК', '(ЛК) Стандартный заказ на кухни'),
        ('ЭШ', '(ЭШ) Стандартный заказ на шкафы'),
        ('П', '(П) Порталы')
    ]

    SUB_ORDER_TYPES = [
        ('ДОП', 'Дополнительный заказ'),
        ('РЕК', 'Рекламация'),
        ('ДОД', 'Доделка'),
    ]

    # Основные поля заказа
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='orders', verbose_name='Заказчик'
    )
    order_number = models.CharField(
        max_length=50, unique=True, verbose_name='Номер заказа', blank=True
    )
    month = models.IntegerField(verbose_name='Месяц заказа')
    year = models.IntegerField(verbose_name='Год заказа')
    week = models.IntegerField(verbose_name='Производственная неделя')

    manager = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='managed_orders',
        limit_choices_to={'department__name': 'коммерческий'}, verbose_name='Менеджер'
    )

    parent_order = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sub_orders', verbose_name='Родительский заказ'
    )

    order_type = models.CharField(
        max_length=3, choices=ORDER_TYPES, null=True, blank=True, verbose_name='Тип заказа'
    )
    sub_order_type = models.CharField(
        max_length=3, choices=SUB_ORDER_TYPES, null=True, blank=True,
        verbose_name='Тип доп. заказа'
    )

    weight = models.FloatField(blank=True, null=True, verbose_name='Масса')
    package_count = models.IntegerField(blank=True, null=True, verbose_name='Количество упаковок')
    start_date = models.DateField(blank=True, null=True, verbose_name='Дата начала обработки')

    technologist = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_orders',
        limit_choices_to={'department__name': 'конструкторский'}, verbose_name='Исполнитель'
    )

    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='accepted', verbose_name='Статус заказа'
    )

    has_mdf = models.BooleanField(default=False, verbose_name='МДФ')
    has_fittings = models.BooleanField(default=False, verbose_name='Фурнитура')
    has_glass = models.BooleanField(default=False, verbose_name='Стекла')
    has_cnc = models.BooleanField(default=False, verbose_name='ЧПУ')

    ldsp_agt_area = models.FloatField(null=True, blank=True, verbose_name='ЛДСП 16-25мм, АГТ')
    mdf_area = models.FloatField(null=True, blank=True, verbose_name='МДФ')
    edge_04_length = models.FloatField(null=True, blank=True, verbose_name='Кромка 0,4мм')
    edge_2_length = models.FloatField(null=True, blank=True, verbose_name='Кромка 2мм')
    edge_1_length = models.FloatField(null=True, blank=True, verbose_name='Кромка 1мм')

    total_area = models.FloatField(null=True, blank=True, verbose_name='Общая площадь')
    serial_area = models.FloatField(null=True, blank=True, verbose_name='Площадь серийной продукции')
    portal_area = models.FloatField(null=True, blank=True, verbose_name='Площадь каминных порталов')

    reclamation_reason = models.TextField(blank=True, null=True, verbose_name='Причина рекламации')
    part = models.IntegerField(null=True, blank=True, verbose_name='Часть заказа')

    def __str__(self):
        return f"{self.order_number} ({self.get_status_display()})"

    def clean(self):
        if self.sub_order_type and not self.parent_order:
            raise ValidationError({'parent_order': 'Для дополнительных заказов необходимо указать родительский заказ.'})
        if self.week and self.week > 5:
            raise ValidationError({'week': 'Неделя не может быть больше 5'})

    def save(self, *args, **kwargs):
        if not self.pk:  # Только при создании нового заказа
            self.year = datetime.now().year  # Устанавливаем текущий год

            client_code = self.customer.code
            order_type = self.order_type

            # Получаем порядковый номер последнего заказа этого клиента в текущем году
            last_order = Order.objects.filter(
                customer=self.customer,
                year=self.year
            ).order_by('-order_number').first()

            if last_order:
                last_order_number = last_order.order_number.split('-')[-1]
                order_number_part = int(''.join(filter(str.isdigit, last_order_number))) + 1
            else:
                order_number_part = 1

            # Формируем базовый номер заказа
            order_number_base = f"{client_code}-{self.year % 100}-{order_number_part:03d}{order_type}"

            # Добавляем дополнительные суффиксы при необходимости
            if self.sub_order_type:
                self.order_number = f"{order_number_base}-{self.sub_order_type}"
            elif self.part:
                self.order_number = f"{order_number_base}-{self.part}"
            else:
                self.order_number = order_number_base

        # Проверяем, что указан тип заказа для основного заказа
        if not self.order_type:
            raise ValueError("Для основных заказов необходимо указать тип заказа.")

        super().save(*args, **kwargs)


class OrderFile(models.Model):
    """
    Модель для хранения файлов, прикрепленных к заказам.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='files', verbose_name='Заказ')
    file = models.FileField(upload_to='order_files/', verbose_name='Файл')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    def __str__(self):
        return f"File for {self.order.order_number}: {self.file.name}"


class OrderComment(models.Model):
    """
    Модель для хранения комментариев к заказам.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comments', verbose_name='Заказ')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.order.order_number}"
