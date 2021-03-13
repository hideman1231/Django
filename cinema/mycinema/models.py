from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone

months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Майа', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']


class MyUser(AbstractUser):
    total_price = models.PositiveIntegerField(verbose_name='Сумма', default=0)


class CinemaHall(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя зала')
    size = models.PositiveSmallIntegerField(verbose_name='Размер зала')

    def __str__(self):
        return self.name


class Session(models.Model):
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='sessions', verbose_name='Зал')
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    show_date = models.CharField(max_length=50, verbose_name='Дата показа', blank=True)
    price = models.PositiveSmallIntegerField(verbose_name='Цена билета')
    status = models.BooleanField(default=True, verbose_name='Статус')

    def get_show_date(self):
        self.show_date = f'С {self.start_time.day} {months[self.start_time.month]} {self.start_time.year} года по {self.end_time.day} {months[self.end_time.month]} {self.end_time.year} года'
        return self.show_date

    def check_status(self):
        if self.end_time < timezone.now():
            self.status = False
        return self.status

    def save(self, *args, **kwargs):
        self.get_show_date()
        self.check_status()
        super().save(*args, **kwargs)


class Ticket(models.Model):
    customer = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='purchased_tickets', verbose_name='Покупатель')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_tickets', verbose_name='Сеанс')