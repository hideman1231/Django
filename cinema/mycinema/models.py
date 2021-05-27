from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone
from rest_framework.authtoken.models import Token


months = [
    'Января',
    'Февраля',
    'Марта',
    'Апреля',
    'Майа',
    'Июня',
    'Июля',
    'Августа',
    'Сентября',
    'Октября',
    'Ноября',
    'Декабря'
]


class MyUser(AbstractUser):
    total_price = models.PositiveIntegerField(verbose_name='Сумма', default=0, blank=True)


class CinemaHall(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя зала')
    size = models.PositiveSmallIntegerField(verbose_name='Размер зала')

    def __str__(self):
        return self.name


class Session(models.Model):
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='sessions', verbose_name='Зал')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    price = models.PositiveSmallIntegerField(verbose_name='Цена билета')
    status = models.BooleanField(default=True, verbose_name='Статус', blank=True)

    @property
    def get_show_date(self):
        return f'С {self.start_date.day} ' \
               f'{months[self.start_date.month - 1]} ' \
               f'{self.start_date.year} года по {self.end_date.day} ' \
               f'{months[self.end_date.month - 1]} {self.end_date.year} года'

    def check_status(self):
        if self.end_date < timezone.now().date():
            self.status = False
        return self.status

    def __str__(self):
        return f'Session {self.id}'

    def save(self, *args, **kwargs):
        self.check_status()
        super().save(*args, **kwargs)


class Ticket(models.Model):
    customer = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='purchased_tickets',
        verbose_name='Покупатель', blank=True
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='session_tickets',
        verbose_name='Сеанс',
        blank=True
    )
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество билетов')

    def __str__(self):
        return f'Ticket {self.id}'


class MyToken(Token):
    time_to_die = models.DateTimeField(default=timezone.now)