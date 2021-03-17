from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from datetime import timedelta
from django.utils import timezone
from mycinema.models import MyUser, CinemaHall, Session, Ticket
from mycinema.forms import MyUserCreationForm, FilterForm
import math


class UserLoginViewTest(TestCase):

    def setUp(self):
        self.data = {'username': 'admin', 'password': '123'}
        self.user = MyUser.objects.create_user(**self.data)
        self.url = reverse('login')

    def test_user_login_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.failUnless(isinstance(response.context['form'], AuthenticationForm))

    def test_user_login_post_succes(self):
        response = self.client.post(self.url, data=self.data, follow=True)
        session = self.client.session['time_action']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue(session, timezone.now())

    def test_user_login_post_succes_redirect(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_user_login_post(self):
        data = {'username': 'admin', 'password': '7weds'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())


class UserRegisterViewTest(TestCase):

    def setUp(self):
        self.url = reverse('register')
        self.data = {'username': 'admin', 'password1': '123', 'password2': '123'}

    def test_user_register_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.failUnless(isinstance(response.context['form'], MyUserCreationForm))

    def test_user_register_post_succes(self):
        response = self.client.post(self.url, data=self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MyUser.objects.count(), 1)

    def test_user_register_post_redirect(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_user_register_post_failure(self):
        data = {'username': 'admin', 'password1': '1df2q', 'password2': 'offfw3'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MyUser.objects.count(), 0)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].errors)


class UserLogoutView(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='admin', password='123')
        self.client.force_login(self.user)
        self.url = reverse('logout')

    def test_user_logout_get(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_user_logout_get_redirect(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))


class SessionListViewTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='admin', password='123')
        self.client.force_login(self.user)
        self.url = reverse('index')
        self.cinema_hall = CinemaHall.objects.create(name='One', size=10)
        self.session1 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=(timezone.now() - timedelta(hours=10)).time(),
                                              end_time=(timezone.now() - timedelta(hours=8)).time(),
                                              start_date=timezone.now().date(),
                                              end_date=(timezone.now() + timedelta(days=5)).date(),
                                              price=500)
        self.session2 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=(timezone.now() - timedelta(hours=7)).time(),
                                              end_time=(timezone.now() - timedelta(hours=6)).time(),
                                              start_date=timezone.now().date(),
                                              end_date=(timezone.now() + timedelta(days=5)).date(),
                                              price=700)
        self.session3 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=(timezone.now() - timedelta(hours=3)).time(),
                                              end_time=(timezone.now() - timedelta(hours=2)).time(),
                                              start_date=timezone.now().date(),
                                              end_date=(timezone.now() + timedelta(days=5)).date(),
                                              price=100)
        self.session4 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=timezone.now().time(),
                                              end_time=(timezone.now() + timedelta(hours=2)).time(),
                                              start_date=(timezone.now() + timedelta(days=10)).date(),
                                              end_date=(timezone.now() + timedelta(days=20)).date(),
                                              price=900)
        self.session5 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=(timezone.now() + timedelta(hours=10)).time(),
                                              end_time=(timezone.now() + timedelta(hours=12)).time(),
                                              start_date=(timezone.now() - timedelta(days=1)).date(),
                                              end_date=(timezone.now() + timedelta(days=8)).date(),
                                              price=200)

    def test_session_list_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_session_list_get_paginate_queryset(self):
        response = self.client.get(self.url)
        sessions = Session.objects.filter(status=True, end_date__gte=timezone.now().date(), start_date__lte=timezone.now().date()).count()
        pages = math.ceil(sessions / response.context['paginator'].per_page)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['paginator'].num_pages, pages)
        self.assertEqual(response.context['paginator'].count, sessions)

    def test_session_list_get_filter(self):
        data = {'filter_price': True}
        response = self.client.get(self.url, data=data) 
        sessions_filter = Session.objects.filter(status=True, end_date__gte=timezone.now().date(), start_date__lte=timezone.now().date()).order_by('price')[:3]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'], FilterForm)
        self.assertQuerysetEqual(response.context['sessions'], [repr(i) for i in sessions_filter])

    def test_session_list_get_no_login(self):
        data = {'filter_price': True}
        self.client.logout()
        sessions_filter = Session.objects.filter(status=True, end_date__gte=timezone.now().date(), start_date__lte=timezone.now().date())[:3]
        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('filter' in response.context)
        self.assertEqual(list(response.context['sessions']), list(sessions_filter))