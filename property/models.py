from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


class Flat(models.Model):
    created_at = models.DateTimeField(
        'Когда создано объявление',
        default=timezone.now,
        db_index=True)

    description = models.TextField('Текст объявления', blank=True)
    price = models.IntegerField('Цена квартиры', db_index=True)

    town = models.CharField(
        'Город, где находится квартира',
        max_length=50,
        db_index=True)
    town_district = models.CharField(
        'Район города, где находится квартира',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное')
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4')
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж')

    rooms_number = models.IntegerField(
        'Количество комнат в квартире',
        db_index=True)
    living_area = models.IntegerField(
        'количество жилых кв.метров',
        null=True,
        blank=True,
        db_index=True)

    has_balcony = models.NullBooleanField('Наличие балкона', db_index=True)
    active = models.BooleanField('Активно-ли объявление', db_index=True)
    construction_year = models.IntegerField(
        'Год постройки здания',
        null=True,
        blank=True,
        db_index=True)
    new_building = models.BooleanField(
        'Новостройка',
        null=True,
        blank=True,
        db_index=True
    )

    liked_by = models.ManyToManyField(
        User,
        related_name="liked_flats",
        verbose_name="Кто лайкнул",
        blank=True,
        help_text="Кто лайкнул эту квартиру",
    )

    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'


class Complaint(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='complaints_from',
        verbose_name='Кто жаловался',
        db_index=True,
    )
    flat = models.ForeignKey(
        Flat,
        on_delete=models.CASCADE,
        related_name='complaints_to',
        verbose_name='Квартира, на которую пожалвались',
    )
    text = models.TextField('Текст жалобы', help_text='Текст жалобы')

    def __str__(self):
        return f'Жалоба от {self.user} на квартиру {self.flat}'


class Owner(models.Model):
    full_name = models.CharField('ФИО владельца', max_length=200)
    phone_number = models.CharField('Номер владельца', max_length=20)
    pure_phone_number = PhoneNumberField(
        verbose_name='Нормализованный номер владельца',
        null=True,
        blank=True,
        db_index=True,
        help_text='Номер владельца в международном формате',
        region="RU",
    )
    flats = models.ManyToManyField(
        Flat,
        related_name='owners',
        verbose_name='Квартиры',
        blank=True,
        help_text='Квартиры в собственности',
    )

    def __str__(self):
        return self.full_name
