from django.db import models


class UserProfile(models.Model):
    tg = models.BigIntegerField(verbose_name="Telegram ID", primary_key=True)
    username = models.CharField(verbose_name="Telegram Username", max_length=255, blank=True, null=True)
    fullname = models.CharField(verbose_name="Полное имя", max_length=255, blank=True, null=True)
    contact = models.CharField(verbose_name="Номер телефона", max_length=255, blank=True, null=True)
    region = models.CharField(verbose_name="Регион проживания", max_length=255, blank=True, null=True)
    city = models.CharField(verbose_name="Населенный пункт", max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.fullname} - ID: {self.tg}"

    class Meta:
        verbose_name = 'пользователи бота'
        verbose_name_plural = 'Пользователи бота'


class Category(models.Model):
    category = models.CharField(verbose_name="Категория", max_length=30, primary_key=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'категории объявлений'
        verbose_name_plural = 'Категории объявлений'


class Advert(models.Model):
    id = models.AutoField(verbose_name='Уникальный ID', primary_key=True)
    date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    author = models.ForeignKey(UserProfile, verbose_name='Автор объявления', on_delete=models.CASCADE)
    region = models.CharField(verbose_name='Регион объявления', max_length=100)
    city = models.CharField(verbose_name="Населенный пункт объявления", max_length=100)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    photos = models.TextField(verbose_name="ID медиафайлов")
    caption = models.CharField(verbose_name="Описание", max_length=1024)
    delivery = models.BooleanField(verbose_name="Готовность отправить доставку", default=False)
    payer_choices = [
        ('User', 'Пользователь'),
        ('Author', 'Владелец'),
    ]
    payer = models.CharField(verbose_name="Выбор отправителя", max_length=20, choices=payer_choices)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'объявления'
        verbose_name_plural = 'Объявления'


class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="Пользователь", on_delete=models.CASCADE)
    ad = models.ForeignKey(Advert, verbose_name="Объявление", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.ad}"

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="Пользователь", on_delete=models.CASCADE)
    ad = models.ForeignKey(Advert, verbose_name="Объявление", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст отзыва")

    def __str__(self):
        return f"{self.user} - {self.ad}"

    class Meta:
        verbose_name = 'отзывы'
        verbose_name_plural = 'Отзывы'


class BlockedUsers(models.Model):
    blocked_user = models.ForeignKey(UserProfile, verbose_name="Заблокированный пользователь", on_delete=models.CASCADE)
    reason = models.TextField(verbose_name="Причина блокировки")

    def __str__(self):
        return f"{self.blocked_user} - {self.reason}"

    class Meta:
        verbose_name = 'заблокированные пользователи'
        verbose_name_plural = 'Заблокированные пользователи'
