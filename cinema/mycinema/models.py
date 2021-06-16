from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext, gettext_lazy as _, ngettext_lazy


months = [
    _('January'),
    _('February'),
    _('March'),
    _('April'),
    _('May'),
    _('June'),
    _('July'),
    _('August'),
    _('September'),
    _('October'),
    _('November'),
    _('December')
]


class MyUser(AbstractUser):
    total_price = models.PositiveIntegerField(verbose_name=_('Amount'), default=0, blank=True)


class CinemaHall(models.Model):

    class Meta:
        verbose_name = _('Hall')
        verbose_name_plural = _('Halls')

    name = models.CharField(max_length=50, verbose_name=_('Hall name'))
    size = models.PositiveSmallIntegerField(verbose_name=_('Hall size'))

    def __str__(self):
        return self.name


class Session(models.Model):

    class Meta:
        verbose_name = _('Session')
        verbose_name_plural = _('Sessions')

    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='sessions', verbose_name=_('Hall'))
    start_time = models.TimeField(verbose_name=_('Start time'))
    end_time = models.TimeField(verbose_name=_('End time'))
    start_date = models.DateField(verbose_name=_('Start date'))
    end_date = models.DateField(verbose_name=_('End date'))
    price = models.PositiveSmallIntegerField(verbose_name=_('Ticket price'))
    status = models.BooleanField(default=True, verbose_name=_('Status'), blank=True)

    @property
    def get_show_date(self):
        return f'С {self.start_date.day} ' \
               f'{months[self.start_date.month - 1]} ' \
               f'{self.start_date.year} ' \
               f"{_('of the year to ')}" \
               f'{self.end_date.day} ' \
               f'{months[self.end_date.month - 1]} {self.end_date.year} ' \
               f"{_('of the year')}"

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

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    customer = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='purchased_tickets',
        verbose_name=_('Purchase'), blank=True
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='session_tickets',
        verbose_name=_('Session'),
        blank=True
    )
    quantity = models.PositiveSmallIntegerField(verbose_name=_('Quantity ticket'))

    def __str__(self):
        return f'Ticket {self.id}'


class MyToken(Token):
    time_to_die = models.DateTimeField(default=timezone.now)
