from datetime import timedelta, time
from django.test import TestCase
from django.utils import timezone
from mycinema.models import MyUser, CinemaHall, Session, Ticket, months


class SessionTest(TestCase):

    def setUp(self):
        self.cinema_hall = CinemaHall.objects.create(name='One', size=25)
        self.session = Session.objects.create(hall=self.cinema_hall,
                                              start_time=time(9, 40, 41),
                                              end_time=time(11, 40, 41),
                                              start_date=timezone.now().date(),
                                              end_date=(timezone.now() + timedelta(days=5)).date(),
                                              price=200)

    def test_get_show_date(self):
        show_date = f'С {self.session.start_date.day} {months[self.session.start_date.month - 1]} {self.session.start_date.year} года по {self.session.end_date.day} {months[self.session.end_date.month - 1]} {self.session.end_date.year} года'
        self.assertEqual(self.session.get_show_date, show_date)
