from rest_framework.test import APITestCase
from mycinema.models import MyUser, CinemaHall, Session, Ticket
from datetime import timedelta
from django.utils import timezone
from datetime import timedelta, time, datetime
from mycinema.api.serializers import (MyUserRegisterSerializer, CinemaHallSerializer, SessionCreateSerializer,
                                    SessionUpdateSerializer, TicketSerializer)
from .factories import UserFactory, CinemaHallFactory, SessionFactory, TicketFactory


class MyUserRegisterSerializerTest(APITestCase):

    def test_user_register_succes(self):
        data = {
            'username': 'admin',
            'password': 1,
            'password2': 1
        }
        serializer = MyUserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_user_register_failure(self):
        data = {
            'username': 'admin',
            'password': 1,
            'password2': 2
        }
        serializer = MyUserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'], ['Пароли не совпадают'])


class CinemaHallSerializerTest(APITestCase):

    def test_create_cinema_hall_succes(self):
        data = {
            'name': 'one',
            'size': 12
        }
        serializer = CinemaHallSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class SessionCreateSerializerTest(APITestCase):

    def setUp(self):
        self.cinema_hall = CinemaHallFactory()
        SessionFactory(hall=self.cinema_hall,
                       start_time=time(8, 40, 41),
                       end_time=time(10, 40, 41),
                       price=50)

    def test_create_session_succes(self):
        data = {
            'hall': self.cinema_hall.pk,
            'start_time': time(12, 40, 41),
            'end_time': time(16, 40, 41),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=2)).date(),
            'price': 50
        }
        serializer = SessionCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_create_session_failure(self):
        data = {
            'hall': self.cinema_hall.pk,
            'start_time': time(6, 40, 41),
            'end_time': time(16, 40, 41),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=2)).date(),
            'price': 50
        }
        serializer = SessionCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'], ['Зал в это время занят'])


class SessionUpdateSerializerTest(APITestCase):

    def setUp(self):
        self.cinema_hall = CinemaHallFactory()
        self.session = SessionFactory(hall=self.cinema_hall,
                       start_time=time(8, 40, 41),
                       end_time=time(10, 40, 41),
                       price=20)
        SessionFactory(hall=self.cinema_hall,
                       start_time=time(12, 40, 41),
                       end_time=time(14, 40, 41),
                       price=50)

    def test_update_session_succes(self):
        data = {
            'hall': self.cinema_hall.pk,
            'start_time': time(16, 40, 41),
            'end_time': time(18, 40, 41),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=2)).date(),
            'price': 50
        }
        serializer = SessionUpdateSerializer(instance=self.session, data=data)
        self.assertTrue(serializer.is_valid())

    def test_update_session_succes(self):
        data = {
            'hall': self.cinema_hall.pk,
            'start_time': time(10, 40, 41),
            'end_time': time(18, 40, 41),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=2)).date(),
            'price': 50
        }
        serializer = SessionUpdateSerializer(instance=self.session, data=data)
        self.assertFalse(serializer.is_valid())


class TicketSerializerTest(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.cinema_hall = CinemaHallFactory()
        self.session = SessionFactory(hall=self.cinema_hall,
                                      start_time=time(8, 40, 41),
                                      end_time=time(10, 40, 41),
                                      price=20)

    def test_create_ticket_succes(self):
        data = {
            'customer': self.user.pk,
            'session': self.session.pk,
            'quantity': 5
        }
        serializer = TicketSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_create_ticket_failure(self):
        data = {
            'customer': self.user.pk,
            'session': self.session.pk,
            'quantity': 50
        }
        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'], [f'Мест не хватает! Свободных мест: {self.cinema_hall.size}'])