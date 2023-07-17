from django.db import models


class UserProfile(models.Model):
    tg = models.BigIntegerField(verbose_name="Telegram ID", primary_key=True)
    username = models.CharField(verbose_name="Telegram Username", max_length=255, blank=True, null=True)
    fullname = models.CharField(verbose_name="Полное имя", max_length=255, blank=True, null=True)
    contact = models.CharField(verbose_name="Номер телефона", max_length=255, blank=True, null=True)
    region = models.CharField(verbose_name="Регион проживания", max_length=255, blank=True, null=True)
    city = models.CharField(verbose_name="Населенный пункт", max_length=255, blank=True, null=True)
    rating = models.FloatField(verbose_name="Рейтинг", default=0)

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
    payer_choices = [('User', 'Пользователь'),
                     ('Author', 'Владелец')]
    status_choices = [('active', 'Активное объявление'),
                      ('agreement', 'Найден получатель'),
                      ('confirm', 'Вещи переданы')]
    id = models.AutoField(verbose_name='ID', primary_key=True)
    date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    author = models.ForeignKey(UserProfile, verbose_name='Автор объявления', on_delete=models.CASCADE)
    region = models.CharField(verbose_name='Регион объявления', max_length=100)
    city = models.CharField(verbose_name="Населенный пункт объявления", max_length=100)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    photos = models.TextField(verbose_name="ID медиафайлов")
    caption = models.CharField(verbose_name="Описание", max_length=1024)
    delivery = models.BooleanField(verbose_name="Готовность отправить доставку", default=False)
    payer = models.CharField(verbose_name="Выбор отправителя", max_length=20,
                             choices=payer_choices, blank=True, null=True)
    status = models.CharField(verbose_name="Статус", max_length=30, choices=status_choices, default='active')

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
        unique_together = ('user', 'ad')


class Review(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name="Автор", on_delete=models.CASCADE, null=True)
    user_id = models.BigIntegerField(verbose_name="Пользователь", null=True)
    text = models.TextField(verbose_name="Текст отзыва")

    def __str__(self):
        return f"{self.author} - {self.text}"

    class Meta:
        verbose_name = 'отзывы'
        verbose_name_plural = 'Отзывы'


class BlockedUsers(models.Model):
    blocked_user = models.OneToOneField(
        UserProfile, verbose_name="Заблокированный пользователь", on_delete=models.CASCADE, unique=True)
    reason = models.TextField(verbose_name="Причина блокировки")

    def __str__(self):
        return f"{self.blocked_user} - {self.reason}"

    class Meta:
        verbose_name = 'заблокированные пользователи'
        verbose_name_plural = 'Заблокированные пользователи'


class ExplicitWords(models.Model):
    word = models.CharField(verbose_name="Запрещённое слово", max_length=40)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'запрещенные слова'
        verbose_name_plural = 'Запрещенные слова'


class Agreements(models.Model):
    user_id = models.BigIntegerField(verbose_name="Пользователь")
    author = models.ForeignKey(UserProfile, verbose_name="Автор объявления", on_delete=models.CASCADE)
    ad = models.ForeignKey(Advert, verbose_name="Объявление", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} - {self.user_id}"

    class Meta:
        verbose_name = 'договоренности'
        verbose_name_plural = 'Договоренности'


class SendMessage(models.Model):
    type_choices = [('ad', 'Реклама'),
                    ('admin', 'Администраторское'),
                    ('regular', 'Без пометок')]
    message_type = models.CharField(verbose_name='Тип сообщения', choices=type_choices, null=False, default='regular')
    text = models.CharField(verbose_name="Текст сообщения", max_length=244, null=False)
    image = models.ImageField(verbose_name="Прикрепленная картинка", blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'Отправить сообщение всем пользователям'


class UserRating(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="Имя пользователя", on_delete=models.CASCADE)
    grade = models.IntegerField(verbose_name='Оценка', blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.grade}"

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'Оценки'
