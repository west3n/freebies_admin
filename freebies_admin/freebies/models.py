from django.db import models


class UserProfile(models.Model):
    tg = models.BigIntegerField(verbose_name="Telegram ID", primary_key=True)
    username = models.CharField(verbose_name="Telegram Username", max_length=255, blank=True, null=True)
    fullname = models.CharField(verbose_name="Полное имя", max_length=255, blank=True, null=True)
    contact = models.CharField(verbose_name="Номер телефона", max_length=255, blank=True, null=True)
    region = models.CharField(verbose_name="Регион проживания", max_length=255, blank=True, null=True)
    city = models.CharField(verbose_name="Населенный пункт", max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - ID: {self.tg}"

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'
