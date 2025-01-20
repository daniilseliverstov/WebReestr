from django.test import TestCase
from .models import Department, Profile
from django.contrib.auth.models import User


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
