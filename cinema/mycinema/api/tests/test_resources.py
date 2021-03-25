from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from mycinema.models import MyUser, CinemaHall, Session, Ticket, MyToken
from datetime import timedelta
from .factories import SessionFactory


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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ['Пароли не совпадают'])


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
        2 = len(response.data['results'])

        breakpoint()


