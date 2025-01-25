from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Customer
from users.models import Department, CustomUser


class CustomerModelTest(TestCase):
    def setUp(self):
        self.commercial_department = Department.objects.create(name="Коммерческий")
        self.design_department = Department.objects.create(name="Конструкторский")
        self.manager = CustomUser.objects.create_user(username='manager', password='password',
                                                      department=self.commercial_department)
        self.non_manager = CustomUser.objects.create_user(username='non_manager', password='password',
                                                          department=self.design_department)

    def test_customer_creation(self):
        """Проверяет создание заказчика."""
        customer = Customer.objects.create(name="ООО 'Рога и Копыта'", city="Москва", code="РИК", manager=self.manager)
        self.assertEqual(customer.name, "ООО 'Рога и Копыта'")
        self.assertEqual(customer.city, "Москва")
        self.assertEqual(customer.code, "РИК")
        self.assertEqual(customer.manager, self.manager)
        self.assertEqual(str(customer), "ООО 'Рога и Копыта' (РИК)")

    def test_customer_unique_code(self):
        """Проверяет уникальность кода заказчика."""
        Customer.objects.create(name="ООО 'Рога и Копыта'", city="Москва", code="РИК", manager=self.manager)
        with self.assertRaises(Exception):
            Customer.objects.create(name="ООО 'Рога и Копыта'", city="Москва", code="РИК", manager=self.manager)

    def test_customer_manager_from_commercial(self):
        """Проверяет, что менеджер из коммерческого отдела."""
        customer = Customer(name="ООО 'Другая компания'", city="Санкт-Петербург", code="ДК", manager=self.non_manager)
        with self.assertRaises(ValidationError) as context:
            customer.full_clean()
        self.assertIn('manager', context.exception.message_dict)
        self.assertEqual(context.exception.message_dict['manager'][0], 'Менеджер должен быть из коммерческого отдела.')
