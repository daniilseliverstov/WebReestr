from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, datetime
from .models import Order, OrderFile, OrderComment
from users.models import Department, CustomUser
from customers.models import Customer


class OrderModelTest(TestCase):
    def setUp(self):
        self.commercial_department = Department.objects.create(name="Коммерческий")
        self.design_department = Department.objects.create(name="Конструкторский")
        self.manager = CustomUser.objects.create_user(username='manager', password='password',
                                                      department=self.commercial_department)
        self.technologist = CustomUser.objects.create_user(username='technologist', password='password',
                                                           department=self.design_department)
        self.customer = Customer.objects.create(name="ООО 'Рога и Копыта'", city="Москва", code="РИК",
                                                manager=self.manager)

    def test_order_creation_with_number_generation(self):
        """Проверяет создание заказа с автоматической генерацией номера."""
        original_year = datetime.now().year
        order1 = Order.objects.create(
            customer=self.customer,
            month=10,
            week=4,
            manager=self.manager,
            start_date=date(2024, 10, 1),
            technologist=self.technologist,
            order_type='Н',
            status='accepted'
        )
        # Проверяем, что номер заказа начинается с кода клиента и года
        self.assertTrue(order1.order_number.startswith(f"{self.customer.code}-{original_year % 100}-"))
        # Проверяем, что номер заказа имеет правильную структуру
        self.assertEqual(len(order1.order_number.split('-')), 3)  # Формат: КОД-ГОД-НОМЕР

        order2 = Order.objects.create(
            customer=self.customer,
            month=10,
            week=4,
            manager=self.manager,
            start_date=date(2024, 10, 1),
            technologist=self.technologist,
            order_type='Н',
            status='accepted'
        )
        # Проверяем, что номер второго заказа увеличился на 1
        order_number_part1 = int(order1.order_number.split('-')[-1][:-1])  # Извлекаем номер из первого заказа
        order_number_part2 = int(order2.order_number.split('-')[-1][:-1])  # Извлекаем номер из второго заказа
        self.assertEqual(order_number_part2, order_number_part1 + 1)

    def test_order_unique_number(self):
        """Проверяет уникальность номера заказа."""
        order = Order.objects.create(
            customer=self.customer,
            month=10,
            week=4,
            manager=self.manager,
            start_date=date(2023, 10, 1),
            technologist=self.technologist,
            order_type='Н',
            status='accepted'
        )
        with self.assertRaises(Exception):
            order2 = Order(
                customer=self.customer,
                month=10,
                week=4,
                manager=self.manager,
                start_date=date(2023, 10, 1),
                technologist=self.technologist,
                order_type='Н',
                status='accepted'
            )
            order2.full_clean()

    def test_order_additional_order_with_parent(self):
        """Проверяет создание доп. заказа с родительским."""
        parent_order = Order.objects.create(
            customer=self.customer,
            month=10,
            week=4,
            manager=self.manager,
            start_date=date(2023, 10, 1),
            technologist=self.technologist,
            order_type='Н',
            status='accepted'
        )
        order = Order.objects.create(
            customer=self.customer,
            month=10,
            week=4,
            manager=self.manager,
            start_date=date(2023, 10, 1),
            technologist=self.technologist,
            sub_order_type='ДОП',
            parent_order=parent_order,
            order_type='Н',
            status='accepted'
        )
        self.assertEqual(order.sub_order_type, 'ДОП')
        self.assertEqual(order.parent_order, parent_order)
        self.assertTrue(order.order_number.endswith('-ДОП'))

    def test_order_additional_order_without_parent(self):
        """Проверяет создание доп. заказа без родительского."""
        order = Order(
            customer=self.customer,
            month=10,
            week=4,
            manager=self.manager,
            start_date=date(2023, 10, 1),
            technologist=self.technologist,
            sub_order_type='ДОП',
            order_type='Н',
            status='accepted'
        )
        with self.assertRaises(ValidationError) as context:
            order.full_clean()
        self.assertEqual(str(context.exception.message_dict['parent_order'][0]),
                         'Для дополнительных заказов необходимо указать родительский заказ.')

    def test_order_with_part(self):
        """Проверяет создание заказа с частью."""
        order = Order.objects.create(
            customer=self.customer,
            month=10,
            week=4,
            manager=self.manager,
            start_date=date(2023, 10, 1),
            technologist=self.technologist,
            order_type='Н',
            part=1,
            status='accepted'
        )
        self.assertTrue(order.order_number.endswith('-1'))

    def test_order_without_order_type(self):
        """Проверяет создание заказа без типа заказа."""
        with self.assertRaises(Exception) as context:
            Order.objects.create(
                customer=self.customer,
                month=10,
                week=4,
                manager=self.manager,
                start_date=date(2023, 10, 1),
                technologist=self.technologist,
                status='accepted'
            )
        self.assertEqual(str(context.exception), "Для основных заказов необходимо указать тип заказа.")

    def test_order_week_validation(self):
        """Проверяет, что неделя не может быть больше 5."""
        order = Order(
            customer=self.customer,
            month=10,
            week=6,
            manager=self.manager,
            start_date=date(2023, 10, 1),
            technologist=self.technologist,
            order_type='Н',
            status='accepted'
        )
        with self.assertRaises(ValidationError) as context:
            order.full_clean()
        self.assertEqual(str(context.exception.message_dict['week'][0]), 'Неделя не может быть больше 5')


class OrderFileModelTest(TestCase):
    def setUp(self):
        self.commercial_department = Department.objects.create(name="Коммерческий")
        self.design_department = Department.objects.create(name="Конструкторский")
        self.manager = CustomUser.objects.create_user(username='manager', password='password',
                                                      department=self.commercial_department)
        self.technologist = CustomUser.objects.create_user(username='technologist', password='password',
                                                           department=self.design_department)
        self.customer = Customer.objects.create(name="ООО 'Рога и Копыта'", city="Москва", code="РИК",
                                                manager=self.manager)
        self.order = Order.objects.create(
            customer=self.customer,
            month=10,
            week=4,
            manager=self.manager,
            start_date=date(2023, 10, 1),
            technologist=self.technologist,
            order_type='Н',
            status='accepted'
        )

    def test_file_upload(self):
        """Проверяет создание файла для заказа."""
        test_file = SimpleUploadedFile('test.txt', b'file_content')
        file = OrderFile.objects.create(order=self.order, file=test_file)
        self.assertEqual(file.order, self.order)
        self.assertEqual(file.file.name, 'order_files/test.txt')  # Проверяем имя файла
        self.assertTrue(file.file.url.startswith('/media/order_files/test.txt'))  # Проверяем URL

    def tearDown(self):
        """Удаляет все файлы после тестов."""
        for order_file in OrderFile.objects.all():
            order_file.file.delete()


class OrderCommentModelTest(TestCase):
    def setUp(self):
        self.commercial_department = Department.objects.create(name="Коммерческий")
        self.design_department = Department.objects.create(name="Конструкторский")
        self.manager = CustomUser.objects.create_user(username='manager', password='password',
                                                      department=self.commercial_department)
        self.technologist = CustomUser.objects.create_user(username='technologist', password='password',
                                                           department=self.design_department)
        self.customer = Customer.objects.create(name="ООО 'Рога и Копыта'", city="Москва", code="РИК",
                                                manager=self.manager)
        self.order = Order.objects.create(
            customer=self.customer,
            month=10,
            week=4,
            manager=self.manager,
            start_date=date(2023, 10, 1),
            technologist=self.technologist,
            order_type='Н',
            status='accepted'
        )

    def test_comment_creation(self):
        """Проверяет создание комментария к заказу."""
        comment = OrderComment.objects.create(order=self.order, user=self.manager, text="test comment")
        self.assertEqual(comment.order, self.order)
        self.assertEqual(comment.user, self.manager)
        self.assertEqual(comment.text, "test comment")
        self.assertTrue(comment.created_at)
        self.assertEqual(str(comment), f"Comment by manager on {self.order.order_number}")
