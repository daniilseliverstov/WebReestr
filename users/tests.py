from django.test import TestCase
from .models import Department, CustomUser


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
