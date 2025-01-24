from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from customers.models import Customer
from users.models import Profile, Department
from orders.models import Orders


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
        """Тест создания заказа."""
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
        """Тест выбора статуса заказа."""
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
        """Тест недопустимого статуса заказа."""
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
        """Тест создания заказа без обязательных полей."""
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

    def test_order_str_method(self):
        """Тест метода __str__ для заказа."""
        order = Orders.objects.create(
            customer=self.customer,
            order_number='TST-24-005Н-1',
            month=1,
            week=1,
            manager=self.profile,
            status='completed'
        )
        self.assertEqual(str(order), 'TST-24-005Н-1 (Готово)')

    def test_order_manager_validation(self):
        """Тест валидации менеджера из коммерческого отдела."""
        # Создаем профиль не из коммерческого отдела
        user2 = User.objects.create_user(username='testuser2', password='12345')
        profile2 = Profile.objects.create(user=user2, department='technical')

        with self.assertRaises(ValidationError):
            order = Orders(
                customer=self.customer,
                order_number='TST-24-006Н-1',
                month=1,
                week=1,
                manager=profile2,  # Менеджер не из коммерческого отдела
                status='accepted'
            )
            order.full_clean()  # Вызовет ValidationError

    def test_order_assigned_to_validation(self):
        """Тест валидации исполнителя из технического или конструкторского отдела."""
        # Создаем профиль не из технического или конструкторского отдела
        user3 = User.objects.create_user(username='testuser3', password='12345')
        profile3 = Profile.objects.create(user=user3, department='supply')

        with self.assertRaises(ValidationError):
            order = Orders(
                customer=self.customer,
                order_number='TST-24-007Н-1',
                month=1,
                week=1,
                manager=self.profile,
                assigned_to=profile3,  # Исполнитель не из технического или конструкторского отдела
                status='accepted'
            )
            order.full_clean()  # Вызовет ValidationError