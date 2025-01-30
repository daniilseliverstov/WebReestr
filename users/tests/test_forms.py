from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase
from django import  forms
from users.forms import CustomAuthenticationForm
from users.models import Department, CustomUser


class UserFormTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя и отдел
        self.department = Department.objects.create(name="Test Department")
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpassword",
            department=self.department
        )

    def test_custom_authentication_form_valid_data(self):
        """Проверяем, что форма авторизации работает с правильными данными."""
        form_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())  # Форма должна быть валидной

    def test_custom_authentication_form_invalid_data(self):
        """Проверяем, что форма авторизации возвращает ошибку при неправильных данных."""
        form_data = {
            "username": "testuser",
            "password": "wrongpassword"  # Неправильный пароль
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())  # Форма должна быть невалидной
        self.assertIn("__all__", form.errors)  # Проверяем наличие ошибки

    def test_custom_authentication_form_empty_data(self):
        """Проверяем, что форма авторизации возвращает ошибку при пустых данных."""
        form_data = {
            "username": "",
            "password": ""
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())  # Форма должна быть невалидной
        self.assertIn("username", form.errors)  # Ошибка для поля username
        self.assertIn("password", form.errors)  # Ошибка для поля password

    def test_custom_authentication_form_widgets(self):
        """Проверяем, что форма использует правильные виджеты."""
        form = CustomAuthenticationForm()
        self.assertIsInstance(form.fields["username"].widget, forms.TextInput)
        self.assertIsInstance(form.fields["password"].widget, forms.PasswordInput)
        self.assertEqual(form.fields["username"].widget.attrs.get("class"), "form-control")
        self.assertEqual(form.fields["password"].widget.attrs.get("class"), "form-control")

    def test_custom_authentication_form_labels(self):
        """Проверяем, что форма использует правильные labels."""
        form = CustomAuthenticationForm()
        self.assertEqual(form.fields["username"].label, "Логин")
        self.assertEqual(form.fields["password"].label, "Пароль")
