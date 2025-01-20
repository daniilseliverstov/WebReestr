from django.core.exceptions import ValidationError
from django.db import models

from users.models import Profile


class Customer(models.Model):
    """Класс описания Заказчиков."""
    name = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    manager = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=False,
                                limit_choices_to={'department': 'commercial'},  # Ограничение выбора
                                verbose_name='Менеджер')

    def __str__(self):
        return f"{self.name} ({self.code})"

    def clean(self):
        """Проверяем, что менеджер из коммерческого отдела."""
        if self.manager and self.manager.department != 'commercial':
            raise ValidationError({'manager': 'Менеджер должен быть из коммерческого отдела.'})

