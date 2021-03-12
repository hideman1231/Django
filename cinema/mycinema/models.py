from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

month = ['Января', 'Февраля', 'Марта', 'Апреля', 'Майа', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']


class MyUser(AbstractUser):
    pass


class CinemaHall(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя зала')
    size = models.PositiveSmallIntegerField(verbose_name='Размер зала')

    def __str__(self):
        return self.name


class Session(models.Model):
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='halls', verbose_name='Зал')
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    show_date = models.CharField(max_length=50, verbose_name='Дата показа', blank=True)
    price = models.PositiveSmallIntegerField(verbose_name='Цена билета')

    def get_show_date(self):
        self.show_date = f'С {self.start_time.day} {month[self.start_time.month]} {self.start_time.year} года по {self.end_time.day} {month[self.end_time.month]} {self.end_time.year} года'
        return self.show_date

    def save(self, *args, **kwargs):
        self.get_show_date()
        super().save(*args, **kwargs)


class Ticket(models.Model):
    customer = models.ForeignKey(MyUser, on_delete=models.SET_NULL, related_name='customers', verbose_name='Покупатель', null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_DEFAULT, related_name='sessions', verbose_name='Сеанс', null=True, delault=Session.price)