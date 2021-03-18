from django.test import TestCase
from mycinema.models import CinemaHall, Session
from mycinema.forms import CreateSessionForm, UpdateSessionForm
from django.utils import timezone
from datetime import timedelta, time

class CreateSessionFormTest(TestCase):

    def setUp(self):
        self.cinema_hall = CinemaHall.objects.create(name='One', size=25)
        self.session = Session.objects.create(hall=self.cinema_hall,
                                              start_time=time(9, 40, 41),
                                              end_time=time(11, 40, 41),
                                              start_date=(timezone.now() - timedelta(days=6)).date(),
                                              end_date=(timezone.now() + timedelta(days=10)).date(),
                                              price=20)

    def test_create_failure(self):
        form_data = {'hall': self.cinema_hall,
                    'start_time': time(5, 40, 41),
                    'end_time': time(10, 40, 41),
                    'start_date': timezone.now().date(),
                    'end_date': (timezone.now() + timedelta(days=5)).date(),
                    'price': 50}
        form = CreateSessionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_succes(self):
        form_data = {'hall': self.cinema_hall,
                    'start_time': time(6, 40, 41),
                    'end_time': time(8, 40, 41),
                    'start_date': (timezone.now() - timedelta(days=2)).date(),
                    'end_date': (timezone.now() + timedelta(days=3)).date(),
                    'price': 50}
        form = CreateSessionForm(data=form_data)
        self.assertTrue(form.is_valid())


class UpdateSessionForm(TestCase):

    def setUp(self):
        self.cinema_hall = CinemaHall.objects.create(name='One', size=25)
        self.session1 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=time(12, 40, 41),
                                              end_time=time(14, 30, 41),
                                              start_date=(timezone.now() - timedelta(days=5)).date(),
                                              end_date=(timezone.now() + timedelta(days=9)).date(),
                                              price=20)
        self.session2 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=time(18, 40, 41),
                                              end_time=time(19, 40, 41),
                                              start_date=(timezone.now() - timedelta(days=3)).date(),
                                              end_date=(timezone.now() + timedelta(days=1)).date(),
                                              price=20)

    def test_update_failure(self):
        form_data = {'hall': self.cinema_hall,
                    'start_time': time(18, 40, 41),
                    'end_time': time(20, 40, 41),
                    'start_date': (timezone.now() - timedelta(days=2)).date(),
                    'end_date': (timezone.now() + timedelta(days=8)).date(),
                    'price': 50}
        # breakpoint()
        # form = UpdateSessionForm(instance=self.session1, data=form_data)
        # self.assertFalse(form.is_valid())

    def test_update_succes(self):
        form_data = {'hall': self.cinema_hall,
                    'start_time': time(15, 40, 41),
                    'end_time': time(16, 40, 41),
                    'start_date': (timezone.now() - timedelta(days=2)).date(),
                    'end_date': (timezone.now() + timedelta(days=8)).date(),
                    'price': 50}
        # form = UpdateSessionForm(instance=self.session1, data=form_data)
        # self.assertTrue(form.is_valid())
