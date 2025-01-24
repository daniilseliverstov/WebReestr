from django.core.exceptions import ValidationError
from django.db import models
from users.models import CustomUser
from customers.models import Customer


class Order(models.Model):
    """
    Модель для представления заказов.

    Атрибуты:
        STATUS_CHOICES (list): Список возможных статусов заказа.
        ORDER_TYPES (list): Список возможных типов заказов.
        SUB_ORDER_TYPES (list): Список возможных типов дополнительных заказов.
        customer (ForeignKey): Связь с моделью Customer.
        order_number (CharField): Уникальный номер заказа.
        month (IntegerField): Месяц заказа.
        week (IntegerField): Производственная неделя.
        manager (ForeignKey): Связь с моделью CustomUser (менеджер).
                            Менеджер должен быть из коммерческого отдела.
        parent_order (ForeignKey): Ссылка на родительский заказ (для доп. заказов).
        order_type (CharField): Тип заказа (из ORDER_TYPES).
        sub_order_type (CharField): Тип дополнительного заказа (из SUB_ORDER_TYPES).
        weight (FloatField): Масса заказа.
        package_count (IntegerField): Количество упаковок.
        start_date (DateField): Дата начала обработки.
        technologist (ForeignKey): Связь с моделью CustomUser (технолог).
                                   Технолог должен быть из конструкторского отдела.
        status (CharField): Статус заказа (из STATUS_CHOICES).
        has_mdf (BooleanField): Признак наличия МДФ.
        has_fittings (BooleanField): Признак наличия фурнитуры.
        has_glass (BooleanField): Признак наличия стекла.
        has_cnc (BooleanField): Признак наличия ЧПУ.
        ldsp_agt_area (FloatField): Площадь ЛДСП 16-25мм, АГТ.
        mdf_area (FloatField): Площадь МДФ.
        edge_04_length (FloatField): Длина кромки 0,4мм.
        edge_2_length (FloatField): Длина кромки 2мм.
        edge_1_length (FloatField): Длина кромки 1мм.
        total_area (FloatField): Общая площадь.
        serial_area (FloatField): Площадь серийной продукции.
        portal_area (FloatField): Площадь каминных порталов.
        reclamation_reason (TextField): Причина рекламации.
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
        ('Н', 'Нестандартные заказы'),
        ('К', 'Нестандартные заказы кухни'),
        ('ЛК', 'Стандартный заказ на кухни'),
        ('ЭШ', 'Стандартный заказ на шкафы'),
        ('П', 'Порталы')
    ]

    SUB_ORDER_TYPES = [
        ('ДОП', 'Дополнительный заказ'),
        ('РЕК', 'Рекламация'),
        ('ДОД', 'Доделка'),
    ]
    # Основные поля заказа
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name='Заказчик')
    order_number = models.CharField(max_length=50, unique=True, verbose_name='Номер заказа')
    month = models.IntegerField(verbose_name='Месяц заказа')
    week = models.IntegerField(verbose_name='Производственная неделя')
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_orders',
                                limit_choices_to={'department__name': 'коммерческий'},
                                verbose_name='Менеджер')
    parent_order = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='sub_orders')
    order_type = models.CharField(max_length=3, choices=ORDER_TYPES, null=True, blank=True, verbose_name='Тип заказа')
    sub_order_type = models.CharField(max_length=3, choices=SUB_ORDER_TYPES, null=True, blank=True,
                                      verbose_name='Тип доп. заказа')
    weight = models.FloatField(blank=True, null=True, verbose_name='Масса')
    package_count = models.IntegerField(blank=True, null=True, verbose_name='Количество упаковок')
    start_date = models.DateField(blank=True, null=True, verbose_name='Дата начала обработки')
    technologist = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='assigned_orders',
                                     limit_choices_to={'department__name': 'конструкторский'},
                                     verbose_name='Исполнитель')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='accepted', verbose_name='Статус заказа')
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

    # Метод для отображения заказа в админке
    def __str__(self):
        """
        Возвращает строковое представление объекта заказа.
        Используется для отображения в админке.
        """
        return f"{self.order_number} ({self.get_status_display()})"

    def clean(self):
        """
        Проверяет, что для дополнительных заказов указан родительский заказ.
        """
        if self.sub_order_type and not self.parent_order:
            raise ValidationError({'parent_order': 'Для дополнительных заказов необходимо указать родительский заказ.'})

    def save(self, *args, **kwargs):
        """
        Переопределяет метод save для проверки типа заказа.
        """
        if not self.pk and not self.order_type:
            raise ValueError("Для основных заказов необходимо указать тип заказа.")

        super().save(*args, **kwargs)


class OrderFile(models.Model):
    """
    Модель для хранения файлов, прикрепленных к заказу.

    Атрибуты:
        order (ForeignKey): Связь с моделью Order.
        file (FileField): Файл заказа.
        uploaded_at (DateTimeField): Дата и время загрузки файла.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='files', verbose_name='Заказ')
    file = models.FileField(upload_to='order_files/', verbose_name='Файл')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    def __str__(self):
        """
        Возвращает строковое представление объекта файла.
        Используется для отображения в админке.
        """
        return f"File for {self.order.order_number}: {self.file.name}"


class OrderComment(models.Model):
    """
    Модель для хранения комментариев к заказу.

    Атрибуты:
        order (ForeignKey): Связь с моделью Order.
        user (ForeignKey): Связь с моделью CustomUser.
        text (TextField): Текст комментария.
        created_at (DateTimeField): Дата и время создания комментария.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comments', verbose_name='Заказ')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        """
        Возвращает строковое представление объекта комментария.
        Используется для отображения в админке.
        """
        return f"Comment by {self.user.username} on {self.order.order_number}"
