from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase
from users.models import Department, CustomUser


class DepartmentModelTest(TestCase):

    def test_department_creation(self):
        """Проверяет создание отдела."""
        department = Department.objects.create(name="Коммерческий")
        self.assertEqual(department.name, "Коммерческий")
        self.assertEqual(str(department), "Коммерческий")

    def test_department_unique_name(self):
        """Проверяет уникальность названия отдела."""
        Department.objects.create(name="Коммерческий")
        with self.assertRaises(Exception):
            Department.objects.create(name="Коммерческий")


class CustomUserModelTest(TestCase):

    def setUp(self):
        self.department = Department.objects.create(name="Конструкторский")
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword",
                                                   department=self.department)

    def test_user_creation(self):
        """Проверяет создание пользователя."""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.department, self.department)
        self.assertEqual(str(self.user), "testuser")


class UserFormTest(TestCase):
    def test_login_form_valid_data(self):
        """Проверяем, что форма авторизации возвращает правильные значения"""
        form = AuthenticationForm(data={"username": "testuser", "password": "testpassword"})
        self.assertFalse(form.is_valid())
        form = AuthenticationForm(data={"username": "testuser", "password": "wrongpassword"})

    def test_login_form_invalid_data(self):
        """Проверяем, что форма авторизации возвращает ошибку при не правильных данных"""
        form = AuthenticationForm(data={"username": "testuser", "password": "wrongpassword"})
        self.assertFalse(form.is_valid())
