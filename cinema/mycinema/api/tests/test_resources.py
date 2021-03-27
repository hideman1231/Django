from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from mycinema.models import MyUser, CinemaHall, Session, Ticket, MyToken
from datetime import timedelta
from .factories import UserFactory, CinemaHallFactory, SessionFactory
from django.utils import timezone
from datetime import timedelta, time


class CustomAuthTokenTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api_token_auth')

    def test_get_user_token_post(self):
        data = {'username': 'a', 'password': '1'}
        user = MyUser.objects.create_user(**data)
        response = self.client.post(self.url, data)
        time_to_die = str(user.auth_token.time_to_die + timedelta(minutes=5))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], user.auth_token.key)
        self.assertEqual(response.data['time_to_die'], time_to_die)

    def test_get_superuser_token_post(self):
        data = {'username': 'admin', 'password': '1'}
        user = MyUser.objects.create_superuser(**data)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], user.auth_token.key)
        self.assertEqual(response.data['time_to_die'], str(None))


class UserRegisterAPIViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api_register')

    def test_user_register_post_succes(self):
        data = {'username': 'a', 'password': '1', 'password2': '1'}
        response = self.client.post(self.url, data)
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_register_post_failure(self):
        data = {'username': 'a', 'password': 'b', 'password2': '1'}
        response = self.client.post(self.url, data)
        self.assertEqual(MyUser.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.data['non_field_errors'], ['Пароли не совпадают'])


class SessionListAPIViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api_sessions')
        SessionFactory()
        SessionFactory()
        SessionFactory()
        SessionFactory()
        SessionFactory()

    def test_session_list_paginate(self):
        response = self.client.get(self.url, {'page': 2})
        # 2 = len(response.data['results'])




class CreateCinemaHallAPIViewTest(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.url = reverse('api_create_cinema_hall')

    def test_create_cinema_hall_post_no_login(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_cinema_hall_post_no_super_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_cinema_hall_post_succes(self):
        self.user.is_staff = True
        self.user.save()
        data = {'name': 'a', 'size': 10}
        response = self.client.post(self.url, data=data)
        self.assertEqual(CinemaHall.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_cinema_hall_post_failure(self):
        self.user.is_staff = True
        self.user.save()
        data = {'name': 'a'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(CinemaHall.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.data['size'], ['This field is required.'])


class CreateCinemaHallAPIViewTest(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.cinema_hall = CinemaHallFactory()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.url = reverse('api_create_session')

    def test_create_session_post_no_login(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_session_post_no_super_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_session_post_no_super_succes(self):
        self.user.is_staff = True
        self.user.save()
        data = {
            'hall': self.cinema_hall.pk,
            'start_time': time(5, 40, 41),
            'end_time': time(10, 40, 41),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=5)).date(),
            'price': 50
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(Session.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_session_post_no_super_failure(self):
        self.user.is_staff = True
        self.user.save()
        data = {
            'hall': self.cinema_hall.pk,
            'start_time': time(5, 40, 41),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=5)).date(),
            'price': 50
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(Session.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)