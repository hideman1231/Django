import math
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from datetime import timedelta
from django.utils import timezone
from mycinema.models import MyUser, CinemaHall, Session, Ticket
from mycinema.forms import (MyUserCreationForm, FilterForm, CreateCinemaHallForm, 
                            CreateSessionForm, QuantityTicketForm, UpdateSessionForm)
from datetime import timedelta, time
from django.db.models import Sum
from datetime import timedelta, datetime
from django.utils import timezone


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
        sessions = Session.objects.filter(status=True, 
            end_date__gte=timezone.now().date(), 
            start_date__lte=timezone.now().date()).count()
        pages = math.ceil(sessions / response.context['paginator'].per_page)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['paginator'].num_pages, pages)
        self.assertEqual(response.context['paginator'].count, sessions)

    def test_session_list_get_filter_price(self):
        data = {'filter_price': True}
        response = self.client.get(self.url, data=data) 
        sessions_filter = Session.objects.filter(status=True, 
            end_date__gte=timezone.now().date(), 
            start_date__lte=timezone.now().date()).order_by('price')[:3]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'], FilterForm)
        self.assertQuerysetEqual(response.context['sessions'], [repr(i) for i in sessions_filter])

    def test_session_list_get_filter_start_time(self):
        data = {'filter_start_time': True}
        response = self.client.get(self.url, data=data)
        sessions_filter = Session.objects.filter(status=True, 
            end_date__gte=timezone.now().date(), 
            start_date__lte=timezone.now().date()).order_by('start_time')[:3]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'], FilterForm)
        self.assertQuerysetEqual(response.context['sessions'], [repr(i) for i in sessions_filter])

    def test_session_list_get_no_login(self):
        data = {'filter_price': True}
        self.client.logout()
        sessions_filter = Session.objects.filter(status=True, 
            end_date__gte=timezone.now().date(), 
            start_date__lte=timezone.now().date())[:3]
        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('filter' in response.context)
        self.assertEqual(list(response.context['sessions']), list(sessions_filter))

class CreateCinemaHallViewTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_superuser(username='admin', password='123')
        self.client.force_login(self.user)
        self.url = reverse('create_cinema_hall')

    def test_create_cinema_hall_get_no_superuser(self):
        self.user.is_superuser = False
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_create_cinema_hall_get_no_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_cinema_hall_get_succes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_cinema_hall.html')
        self.failUnless(isinstance(response.context['form'], CreateCinemaHallForm))

    def test_create_cinema_hall_post_succes(self):
        data = {'name': 'aaa', 'size': 30}
        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CinemaHall.objects.count(), 1)

    def test_create_cinema_hall_post_succes_redirect(self):
        data = {'name': 'aaa', 'size': 30}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_create_cinema_hall_post_failure(self):
        data = {'name': 'aaa'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(CinemaHall.objects.count(), 0)
        self.assertEqual(response.context['form'].errors, {'size': ['This field is required.']})

class CreateSessionViewTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_superuser(username='admin', password='123')
        self.client.force_login(self.user)
        self.url = reverse('create_session')

    def test_create_session_get_no_superuser(self):
        self.user.is_superuser = False
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_create_session_get_no_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_session_get_succes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_session.html')
        self.failUnless(isinstance(response.context['form'], CreateSessionForm))

    def test_create_session_post_succes(self):
        hall = CinemaHall.objects.create(name='ff', size=20)
        data = {
            'hall': hall.pk,
            'start_time': timezone.now().time(),
            'end_time': (timezone.now() + timedelta(hours=1)).time(),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=5)).date(),
            'price': 100
        }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Session.objects.count(), 1)

    def test_create_session_post_falure(self):
        hall = CinemaHall.objects.create(name='ff', size=20)
        data = {
            'hall': hall.pk,
            'start_time': timezone.now().time(),
            'end_time': (timezone.now() + timedelta(hours=1)).time(),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=5)).date(),
            'price': 'gf'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Session.objects.count(), 0)


class CreateTicketViewTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='a', password='123')
        self.client.force_login(self.user)
        self.url = reverse('create_ticket')
        self.cinema_hall = CinemaHall.objects.create(name='One', size=10)
        self.session1 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=(timezone.now() - timedelta(hours=10)).time(),
                                              end_time=(timezone.now() - timedelta(hours=8)).time(),
                                              start_date=timezone.now().date(),
                                              end_date=(timezone.now() + timedelta(days=5)).date(),
                                              price=500)

    def test_create_ticket_no_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_ticket_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.failUnless(isinstance(response.context['form'], QuantityTicketForm))
        self.assertTemplateUsed(response, 'index.html')

    def test_create_ticket_post_succes(self):
        data = {'quantity': 5, 'session':self.session1.pk}
        response = self.client.post(self.url, data=data, follow=True)
        tickets = self.session1.session_tickets.aggregate(Sum('quantity'))['quantity__sum']
        total_price = response.context['user'].total_price
        self.assertEqual(tickets, data['quantity'])
        self.assertEqual(total_price, data['quantity'] * self.session1.price)

    def test_create_ticket_post_succes_redirect(self):
        data = {'quantity': 5, 'session':self.session1.pk}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_create_ticket_post_failure(self):
        data = {'quantity': 13, 'session':self.session1.pk}
        response = self.client.post(self.url, data=data, follow=True)
        tickets = self.session1.session_tickets.count()
        total_price = response.context['user'].total_price
        self.assertEqual(tickets, 0)
        self.assertEqual(total_price, 0)


class UserPurchaseListViewTest(TestCase):

    def setUp(self):
        self.user1 = MyUser.objects.create_user(username='a', password='123')
        self.user2 = MyUser.objects.create_user(username='b', password='1')
        self.client.force_login(self.user1)
        self.url = reverse('purchases')
        self.cinema_hall = CinemaHall.objects.create(name='One', size=10)
        self.session1 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=(timezone.now() - timedelta(hours=10)).time(),
                                              end_time=(timezone.now() - timedelta(hours=8)).time(),
                                              start_date=timezone.now().date(),
                                              end_date=(timezone.now() + timedelta(days=5)).date(),
                                              price=500)
        self.ticket1 = Ticket.objects.create(customer=self.user1, session=self.session1, quantity=1)
        self.ticket2 = Ticket.objects.create(customer=self.user1, session=self.session1, quantity=1)
        self.ticket3 = Ticket.objects.create(customer=self.user1, session=self.session1, quantity=1)
        self.ticket4 = Ticket.objects.create(customer=self.user2, session=self.session1, quantity=2)

    def test_user_purchase_list_no_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_user_purchase_list_paginate_queryset(self):
        response = self.client.get(self.url)
        tickets = Ticket.objects.filter(customer=self.user1).count()
        pages = math.ceil(tickets / response.context['paginator'].per_page)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['paginator'].num_pages, pages)
        self.assertEqual(response.context['paginator'].count, tickets)


class UpdateCinemaHallViewTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_superuser(username='a', password='1')
        self.client.force_login(self.user)
        self.cinema_hall = CinemaHall.objects.create(name='One', size=10)
        self.url = reverse('update_cinema_hall', args=[self.cinema_hall.pk])
        self.session1 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=(timezone.now() - timedelta(hours=10)).time(),
                                              end_time=(timezone.now() - timedelta(hours=8)).time(),
                                              start_date=timezone.now().date(),
                                              end_date=(timezone.now() + timedelta(days=5)).date(),
                                              price=500)
        self.session2 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=(timezone.now() - timedelta(hours=10)).time(),
                                              end_time=(timezone.now() - timedelta(hours=8)).time(),
                                              start_date=timezone.now().date(),
                                              end_date=(timezone.now() + timedelta(days=5)).date(),
                                              price=500)
        self.ticket = Ticket.objects.create(customer=self.user, session=self.session1, quantity=1)

    def test_update_cinema_hall_get_no_superuser(self):
        self.user.is_superuser = False
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_cinema_hall_get_no_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_update_cinema_hall_get(self):
        self.cinema_hall2 = CinemaHall.objects.create(name='two', size=15)
        url = reverse('update_cinema_hall', args=[self.cinema_hall2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_cinema_hall.html')
        self.failUnless(isinstance(response.context['form'], CreateCinemaHallForm))

    def test_update_cinema_hall_post_failure(self):
        data = {'size': 30}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_update_cinema_hall_post_succes(self):
        self.cinema_hall2 = CinemaHall.objects.create(name='two', size=15)
        url = reverse('update_cinema_hall', args=[self.cinema_hall2.pk]) 
        data = {'size': 30}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].size, data['size'])
        

class UpdateSessionViewTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_superuser(username='a', password='1')
        self.client.force_login(self.user)
        self.cinema_hall = CinemaHall.objects.create(name='One', size=10)
        self.session1 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=time(8, 40, 41),
                                              end_time=time(10, 40, 41),
                                              start_date=timezone.now().date(),
                                              end_date=(timezone.now() + timedelta(days=5)).date(),
                                              price=500)
        self.session2 = Session.objects.create(hall=self.cinema_hall,
                                              start_time=time(14, 40, 41),
                                              end_time=time(20, 40, 41),
                                              start_date=timezone.now().date(),
                                              end_date=(timezone.now() + timedelta(days=5)).date(),
                                              price=500)
        self.ticket = Ticket.objects.create(customer=self.user, session=self.session2, quantity=1)
        self.url = reverse('update_session', args=[self.session2.pk])

    def test_update_session_get_no_superuser(self):
        self.user.is_superuser = False
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_session_get_no_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_update_session_get(self):
        url = reverse('update_session', args=[self.session1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_session.html')
        self.failUnless(isinstance(response.context['form'], UpdateSessionForm))

    def test_update_session_post_failure(self):
        data = {
            'hall': self.cinema_hall.pk, 
            'start_time': time(12, 40, 41), 
            'end_time': time(16, 40, 41) , 
            'start_date': (timezone.now() - timedelta(days=2)).date(),
            'end_date': (timezone.now() + timedelta(days=8)).date(),
            'price': 500
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_update_session_post_succes(self):
        data = {
            'hall': self.cinema_hall.pk, 
            'start_time': time(12, 40, 41), 
            'end_time': time(16, 40, 41) , 
            'start_date': (timezone.now() - timedelta(days=2)).date(),
            'end_date': (timezone.now() + timedelta(days=8)).date(),
            'price': 500
        }
        url = reverse('update_session', args=[self.session1.pk])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].hall.pk, data['hall'])
        self.assertEqual(response.context['object'].start_time, data['start_time'])
        self.assertEqual(response.context['object'].end_time, data['end_time'])
        self.assertEqual(response.context['object'].start_date, data['start_date'])
        self.assertEqual(response.context['object'].price, data['price'])

class SessionForTomorrowListViewTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='admin', password='123')
        self.client.force_login(self.user)
        self.url = reverse('sessions_for_tomorrow')
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

    def test_session_for_tomorrow_list_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'session_for_tomorrow.html')

    def test_session_for_tomorrow_list_paginate_queryset(self):
        response = self.client.get(self.url)
        sessions = Session.objects.filter(status=True, end_date__gte=timezone.now().date() + timedelta(days=1), start_date__lte=timezone.now().date() + timedelta(days=1)).count()
        pages = math.ceil(sessions / response.context['paginator'].per_page)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['paginator'].num_pages, pages)
        self.assertEqual(response.context['paginator'].count, sessions)

    def test_session_for_tomorrow_list_get_filter_price(self):
        data = {'filter_price': True}
        response = self.client.get(self.url, data=data) 
        sessions_filter = Session.objects.filter(status=True, 
            end_date__gte=timezone.now().date() + timedelta(days=1), 
            start_date__lte=timezone.now().date() + timedelta(days=1)).order_by('price')[:3]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'], FilterForm)
        self.assertQuerysetEqual(response.context['session_list'], [repr(i) for i in sessions_filter])

    def test_session_for_tomorrow_list_get_filter_start_time(self):
        data = {'filter_start_time': True}
        response = self.client.get(self.url, data=data)
        sessions_filter = Session.objects.filter(status=True, 
            end_date__gte=timezone.now().date() + timedelta(days=1), 
            start_date__lte=timezone.now().date() + timedelta(days=1)).order_by('start_time')[:3]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'], FilterForm)
        self.assertQuerysetEqual(response.context['session_list'], [repr(i) for i in sessions_filter])

    def test_session_for_tomorrow_list_get_no_login(self):
        data = {'filter_price': True}
        self.client.logout()
        sessions_filter = Session.objects.filter(status=True, 
            end_date__gte=timezone.now().date() + timedelta(days=1), 
            start_date__lte=timezone.now().date() + timedelta(days=1))[:3]
        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('filter' in response.context)
        self.assertEqual(list(response.context['session_list']), list(sessions_filter))