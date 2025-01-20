from django.db import models


class Materials(models.Model):
    mdf = models.BooleanField(default=False, verbose_name='МДФ')
    fittings = models.BooleanField(default=False, verbose_name='Фурнитура')
    glass = models.BooleanField(default=False, verbose_name='Стекла')
    cnc = models.BooleanField(default=False, verbose_name='ЧПУ')
    ldsp_area = models.FloatField(blank=True, null=True, verbose_name='ЛДСП 16-25мм, АГТ (м²)')
    mdf_area = models.FloatField(blank=True, null=True, verbose_name='МДФ (м²)')
    edge_04 = models.FloatField(blank=True, null=True, verbose_name='Кромка 0,4мм (м/п)')
    edge_2 = models.FloatField(blank=True, null=True, verbose_name='Кромка 2мм (м/п)')
    edge_1 = models.FloatField(blank=True, null=True, verbose_name='Кромка 1мм (м/п)')
    total_area = models.FloatField(blank=True, null=True, verbose_name='Общая площадь (м²)')
    serial_area = models.FloatField(blank=True, null=True, verbose_name='Площадь серийной продукции (м²)')
    portal_area = models.FloatField(blank=True, null=True, verbose_name='Площадь каминных порталов (м²)')
