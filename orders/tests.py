from django.test import TestCase
from .models import Customer, Orders
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class CustomerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаём отдел
        cls.department = Department.objects.create(name='Коммерческий отдел')

        # Создаём пользователя и профиль для коммерческого отдела
        cls.commercial_user = User.objects.create_user(username='commercial_manager')
        cls.commercial_profile = Profile.objects.create(
            user=cls.commercial_user,
            department='commercial'
        )

        # Создаём пользователя и профиль для другого отдела
        cls.other_user = User.objects.create_user(username='other_manager')
        cls.other_profile = Profile.objects.create(
            user=cls.other_user,
            department='technical'
        )

    def test_customer_creation_with_commercial_manager(self):
        """Проверяем создание заказчика с менеджером из коммерческого отдела."""
        customer = Customer.objects.create(
            name='Тестовый заказчик',
            city='Москва',
            code='TZ',
            manager=self.commercial_profile
        )
        self.assertEqual(customer.manager, self.commercial_profile)

    def test_customer_creation_with_non_commercial_manager(self):
        """Проверяем, что нельзя создать заказчика с менеджером из другого отдела."""
        with self.assertRaises(ValidationError):
            customer = Customer(
                name='Тестовый заказчик',
                city='Москва',
                code='TZ',
                manager=self.other_profile
            )
            customer.full_clean()  # Вызываем валидацию

    def test_customer_creation_without_manager(self):
        """Проверяем, что нельзя создать заказчика без менеджера."""
        with self.assertRaises(ValidationError):
            customer = Customer(
                name='Тестовый заказчик',
                city='Москва',
                code='TZ',
                manager=None
            )
            customer.full_clean()  # Вызываем валидацию

    def test_customer_creation(self):
        """Проверяем создание заказчика."""
        customer = Customer.objects.create(
            name='Тестовый заказчик',
            city='Москва',
            code='TZ',
            manager=self.commercial_profile
        )

        # Проверяем, что заказчик создан
        self.assertEqual(customer.name, 'Тестовый заказчик')
        self.assertEqual(customer.city, 'Москва')
        self.assertEqual(customer.code, 'TZ')
        self.assertEqual(customer.manager, self.commercial_profile)

    def test_customer_str_representation(self):
        """Проверяем строковое представление заказчика."""
        customer = Customer.objects.create(
            name='Тестовый заказчик',
            city='Москва',
            code='TZ',
            manager=self.commercial_profile
        )

        # Проверяем строковое представление заказчика
        self.assertEqual(str(customer), 'Тестовый заказчик (TZ)')

    def test_customer_unique_code(self):
        """Проверяем, что код заказчика уникален."""
        # Создаём заказчика с уникальным кодом
        Customer.objects.create(
            name='Тестовый заказчик',
            city='Москва',
            code='TZ',
            manager=self.commercial_profile
        )

        # Пытаемся создать заказчика с тем же кодом
        with self.assertRaises(Exception):
            Customer.objects.create(
                name='Другой заказчик',
                city='Калуга',
                code='TZ',  # Код должен быть уникальным
                manager=self.commercial_profile
            )

    def test_customer_creation_without_manager(self):
        """Проверяем, что нельзя создать заказчика без менеджера."""
        with self.assertRaises(ValidationError):
            customer = Customer(
                name='Тестовый заказчик',
                city='Москва',
                code='TZ123',
                manager=None
            )
            customer.full_clean()  # Вызываем валидацию


class OrdersModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные
        cls.department = Department.objects.create(name='Коммерческий отдел')
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.profile = Profile.objects.create(user=cls.user, department='commercial')
        cls.customer = Customer.objects.create(
            name='Тестовый заказчик',
            city='Москва',
            code='TST',
            manager=cls.profile
        )

    def test_create_order(self):
        # Создаем заказ
        order = Orders.objects.create(
            customer=self.customer,
            order_number='TST-24-001Н-1',
            month=1,
            week=1,
            manager=self.profile,
            status='accepted'
        )

        # Проверяем, что заказ создан
        self.assertEqual(order.order_number, 'TST-24-001Н-1')
        self.assertEqual(order.status, 'accepted')
        self.assertEqual(order.get_status_display(), 'Принят')

    def test_order_status_choices(self):
        # Проверяем, что статус заказа соответствует выбору
        order = Orders.objects.create(
            customer=self.customer,
            order_number='TST-24-002Н-1',
            month=1,
            week=1,
            manager=self.profile,
            status='in_progress'
        )
        self.assertEqual(order.get_status_display(), 'В работе')

    def test_order_with_invalid_status(self):
        # Проверяем, что нельзя создать заказ с недопустимым статусом
        with self.assertRaises(ValidationError):
            order = Orders(
                customer=self.customer,
                order_number='TST-24-003Н-1',
                month=1,
                week=1,
                manager=self.profile,
                status='invalid_status'
            )
            order.full_clean()  # Вызовет ValidationError, так как статус недопустим

    def test_order_without_required_fields(self):
        # Проверяем, что нельзя создать заказ без обязательных полей
        with self.assertRaises(ValidationError):
            order = Orders(
                customer=self.customer,
                order_number='',  # Пустой номер заказа
                month=1,
                week=1,
                manager=self.profile,
                status='accepted'
            )
            order.full_clean()  # Вызовет ValidationError, так как номер заказа обязателен

    def test_order_material_fields(self):
        # Проверяем поля, связанные с материалами
        order = Orders.objects.create(
            customer=self.customer,
            order_number='TST-24-004Н-1',
            month=1,
            week=1,
            manager=self.profile,
            status='accepted',
            mdf=True,
            fittings=True,
            glass=False,
            cnc=True,
            ldsp_area=10.5,
            mdf_area=5.0,
            edge_04=2.0,
            edge_2=1.5,
            edge_1=3.0,
            total_area=15.5,
            serial_area=7.0,
            portal_area=3.5
        )

        # Проверяем значения полей
        self.assertTrue(order.mdf)
        self.assertTrue(order.fittings)
        self.assertFalse(order.glass)
        self.assertTrue(order.cnc)
        self.assertEqual(order.ldsp_area, 10.5)
        self.assertEqual(order.mdf_area, 5.0)
        self.assertEqual(order.edge_04, 2.0)
        self.assertEqual(order.edge_2, 1.5)
        self.assertEqual(order.edge_1, 3.0)
        self.assertEqual(order.total_area, 15.5)
        self.assertEqual(order.serial_area, 7.0)
        self.assertEqual(order.portal_area, 3.5)

    def test_order_str_method(self):
        # Проверяем метод __str__
        order = Orders.objects.create(
            customer=self.customer,
            order_number='TST-24-005Н-1',
            month=1,
            week=1,
            manager=self.profile,
            status='completed'
        )
        self.assertEqual(str(order), 'TST-24-005Н-1 (Готово)')
