from django.test import TestCase
from mycinema.models import CinemaHall, Session
from mycinema.forms import CreateSessionForm, UpdateSessionForm
from django.utils import timezone
from datetime import timedelta


class CreateSessionFormTest(TestCase):

    def setUp(self):
        self.cinema_hall = CinemaHall.objects.create(name='One', size=25)
        self.session = Session.objects.create(hall=self.cinema_hall,
                                              start_time=(timezone.now() - timedelta(hours=2)).time(),
                                              end_time=(timezone.now() + timedelta(hours=3)).time(),
                                              start_date=(timezone.now() - timedelta(days=6)).date(),
                                              end_date=(timezone.now() + timedelta(days=10)).date(),
                                              price=20)

    def test_create_failure(self):
        form_data = {'hall': self.cinema_hall,
                    'start_time':timezone.now().time(),
                    'end_time': (timezone.now() + timedelta(hours=1)).time(),
                    'start_date': timezone.now().date(),
                    'end_date': (timezone.now() + timedelta(days=5)).date(),
                    'price': 50}
        form = CreateSessionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_succes(self):
        form_data = {'hall': self.cinema_hall,
                    'start_time':(timezone.now() - timedelta(hours=5)).time(),
                    'end_time': (timezone.now() - timedelta(hours=3)).time(),
                    'start_date': (timezone.now() - timedelta(days=2)).date(),
                    'end_date': (timezone.now() + timedelta(days=3)).date(),
                    'price': 50}
        form = CreateSessionForm(data=form_data)
        self.assertTrue(form.is_valid())


class UpdateSessionForm(TestCase):

    def setUp(self):
        self.cinema_hall = CinemaHall.objects.create(name='One', size=25)
        self.session1 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=(timezone.now() - timedelta(hours=2)).time(),
                                              end_time=(timezone.now() + timedelta(hours=1)).time(),
                                              start_date=(timezone.now() - timedelta(days=5)).date(),
                                              end_date=(timezone.now() + timedelta(days=9)).date(),
                                              price=20)
        self.session2 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=(timezone.now() + timedelta(hours=10)).time(),
                                              end_time=(timezone.now() + timedelta(hours=12)).time(),
                                              start_date=(timezone.now() - timedelta(days=3)).date(),
                                              end_date=(timezone.now() + timedelta(days=1)).date(),
                                              price=20)

    def test_update_failure(self):
        form_data = {'hall': self.cinema_hall,
                    'start_time':(timezone.now() + timedelta(hours=11)).time(),
                    'end_time': (timezone.now() + timedelta(hours=13)).time(),
                    'start_date': (timezone.now() - timedelta(days=2)).date(),
                    'end_date': (timezone.now() + timedelta(days=8)).date(),
                    'price': 50}
        # breakpoint()
        # form = UpdateSessionForm(instance=self.session1, data=form_data)
        # self.assertFalse(form.is_valid())

    def test_update_succes(self):
        form_data = {'hall': self.cinema_hall,
                    'start_time':(timezone.now() + timedelta(hours=5)).time(),
                    'end_time': (timezone.now() + timedelta(hours=9)).time(),
                    'start_date': (timezone.now() - timedelta(days=2)).date(),
                    'end_date': (timezone.now() + timedelta(days=8)).date(),
                    'price': 50}
        # form = UpdateSessionForm(instance=self.session1, data=form_data)
        # self.assertTrue(form.is_valid())
