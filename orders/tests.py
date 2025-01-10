from django.test import TestCase
from .models import Department, Profile, Customer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class DepartmentModelTest(TestCase):
    def test_department_create_change(self):
        # Создаём два отдела
        department1 = Department.objects.create(name='Тестовый')
        department2 = Department.objects.create(name='Тестовый2')

        # Получаем все отделы из базы данных
        all_departments = Department.objects.all()

        # Проверяем, что отделы созданы и их количество равно 2
        self.assertEqual(len(all_departments), 2)
        self.assertEqual(all_departments[0].name, department1.name)
        self.assertEqual(all_departments[1].name, department2.name)

        # Изменяем название второго отдела
        department2.name = 'Обновленный'
        department2.save()

        # Обновляем QuerySet, чтобы получить актуальные данные
        updated_departments = Department.objects.all()

        # Проверяем, что название второго отдела изменилось
        self.assertEqual(updated_departments[1].name, 'Обновленный')

        # Удаляем второй отдел
        department2.delete()

        # Обновляем QuerySet, чтобы получить актуальные данные
        remaining_departments = Department.objects.all()

        # Проверяем, что количество отделов уменьшилось до 1
        self.assertEqual(len(remaining_departments), 1)


class ProfileModelTest(TestCase):
    def test_profile_creation(self):
        # Создаём пользователя
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Создаём профиль для пользователя
        profile = Profile.objects.create(
            user=user,
            department='commercial'
        )

        # Проверяем, что профиль создан и связан с пользователем
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.department, 'commercial')

    def test_profile_str_representation(self):
        # Создаём пользователя и профиль
        user = User.objects.create_user(username='testuser', password='testpassword')
        profile = Profile.objects.create(
            user=user,
            department='technical'
        )

        # Проверяем строковое представление профиля
        self.assertEqual(str(profile), 'testuser (technical)')


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
                code='TZ123',
                manager=self.other_profile
            )
            customer.full_clean()  # Вызываем валидацию

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

    def test_customer_creation(self):
            # Создаём заказчика
            customer = Customer.objects.create(
                name='Тестовый заказчик',
                city='Москва',
                code='TZ',
                manager='Маргарита'
            )

            # Проверяем, что заказчик создан
            self.assertEqual(customer.name, 'Тестовый заказчик')
            self.assertEqual(customer.city, 'Москва')
            self.assertEqual(customer.code, 'TZ')
            self.assertEqual(customer.manager, 'Маргарита')

    def test_customer_str_representation(self):
        # Создаём заказчика
        customer = Customer.objects.create(
            name='Тестовый заказчик',
            city='Москва',
            code='TZ',
            manager='Маргарита'
        )

        # Проверяем строковое представление заказчика
        self.assertEqual(str(customer), 'Тестовый заказчик (TZ)')

    def test_customer_unique_code(self):
        # Создаём заказчика с уникальным кодом
        Customer.objects.create(
            name='Тестовый заказчик',
            city='Москва',
            code='TZ',
            manager='Маргарита'
        )

        # Пытаемся создать заказчика с тем же кодом
        with self.assertRaises(Exception):
            Customer.objects.create(
                name='Другой заказчик',
                city='Калуга',
                code='TZ',  # Код должен быть уникальным
                manager='Наталья'
            )


class OrdersModelTest(TestCase):
    pass
