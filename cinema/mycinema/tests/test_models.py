from django.test import TestCase
from django.utils import timezone
from mycinema.models import MyUser, CinemaHall, Session, Ticket
from datetime import timedelta

class SessionTest(TestCase):

    def setUp(self):
        self.cinema_hall = CinemaHall.objects.create(name='One', size=25)
        self.session = Session.objects.create(hall=self.cinema_hall,
                                              start_time=timezone.now().time(),
                                              end_time=(timezone.now() + timedelta(hours=1)).time(),
                                              start_date=timezone.now().date(),
                                              end_date=(timezone.now() + timedelta(days=5)).date(),
                                              price=200)

    def test_get_show_date(self):
      ...
        # self.assertEqual(self.session.get_show_date(), 'С 16 Марта 2021 года по 21 Марта 2021 года')
