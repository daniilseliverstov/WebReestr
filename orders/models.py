from django.db import models


class Department(models.Model):
    """Класс описания Отделов. Состоит только из названия"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employees(models.Model):
    """Класс для сотрудников производства, надо подумать над его структурой
    Возможно будут наследоваться от AbstractUser"""
    pass


class Customer(models.Model):
    """Класс описания Заказчиков.
    Сделаю после написания тестов. СНАЧАЛА ТЕСТЫ!!!!"""
    pass


class Orders(models.Model):
    """Класс заказов, сложно...."""
    pass
