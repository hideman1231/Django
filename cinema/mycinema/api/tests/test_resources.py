from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from mycinema.models import MyUser, CinemaHall, Session, Ticket, MyToken
from datetime import timedelta
from .factories import UserFactory, CinemaHallFactory, SessionFactory, TicketFactory
from django.utils import timezone
from datetime import timedelta, time, datetime
from django.db.models import Sum, Q
from mycinema.api.serializers import (MyUserRegisterSerializer, CinemaHallSerializer, SessionCreateSerializer,
                                    SessionUpdateSerializer, TicketSerializer)


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


class CinemaHallViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.user.is_staff = True
        self.user.save()
        self.hall = CinemaHallFactory()

    def test_cinema_hall_no_login(self):
        self.client.logout()
        data = {'name': 'one', 'size': 20}
        url = reverse('cinema-halls-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cinema_hall_no_superuser(self):
        self.user.is_staff = False
        data = {'name': 'one', 'size': 20}
        url = reverse('cinema-halls-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cinema_hall_post_succes(self):
        data = {'name': 'one', 'size': 20}
        url = reverse('cinema-halls-list')
        response = self.client.post(url, data)
        self.assertEqual(CinemaHall.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cinema_hall_put_succes(self):
        data = {'name': 'one', 'size': 12}
        url = reverse('cinema-halls-detail', args=[self.hall.pk])
        response = self.client.put(url, data)
        hall = CinemaHall.objects.get(id=self.hall.pk)
        self.assertEqual(hall.name, data['name'])
        self.assertEqual(hall.size, data['size'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cinema_hall_put_failure(self):
        session = SessionFactory(hall=self.hall)
        TicketFactory(session=session)
        data = {'name': 'one', 'size': 12}
        url = reverse('cinema-halls-detail', args=[self.hall.pk])
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertIn('You cannot change which hall is occupied', response.data['detail'])

    def test_cinema_hall_patch_succes(self):
        data = {'name': 'one'}
        url = reverse('cinema-halls-detail', args=[self.hall.pk])
        response = self.client.patch(url, data)
        hall = CinemaHall.objects.get(id=self.hall.pk)
        self.assertEqual(hall.name, data['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cinema_hall_patch_failure(self):
        session = SessionFactory(hall=self.hall)
        TicketFactory(session=session)
        data = {'name': 'one'}
        url = reverse('cinema-halls-detail', args=[self.hall.pk])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(response.data['detail'], ['You cannot change which hall is occupied'])


class SessionViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.hall = CinemaHallFactory()
        self.session = SessionFactory(hall=self.hall, start_time=time(2, 10, 00), end_time=time(3, 00, 00))
        SessionFactory(status=False, start_time=time(4, 10, 00), end_time=time(5, 20, 00))
        SessionFactory(price=60, start_time=time(11, 20, 00), end_time=time(13, 40, 00))
        SessionFactory(price=30, start_date=(timezone.now() + timedelta(days=2)).date(),
                       start_time=time(18, 00, 00), end_time=time(19, 00, 00))
        SessionFactory(price=110, hall=self.hall, start_time=time(12, 40, 00), end_time=time(13, 40, 00))

    def test_session_list_pagination(self):
        url = reverse('session-list')
        response = self.client.get(url)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date(),
               start_date__lte=timezone.now().date())
        sessions = Session.objects.filter(q1)[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_session_tomorrow_list_pagination(self):
        url = reverse('session-tomorrow')
        response = self.client.get(url)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date() + timedelta(days=1),
               start_date__lte=timezone.now().date() + timedelta(days=1))
        sessions = Session.objects.filter(q1)[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_session_list_pagination_filter_price(self):
        url = reverse('session-list')
        data = {'price': True}
        response = self.client.get(url, data=data)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date(),
               start_date__lte=timezone.now().date())
        sessions = Session.objects.filter(q1).order_by('price')[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_session_tomorrow_list_pagination_filter_price(self):
        url = reverse('session-tomorrow')
        data = {'price': True}
        response = self.client.get(url, data=data)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date() + timedelta(days=1),
               start_date__lte=timezone.now().date() + timedelta(days=1))
        sessions = Session.objects.filter(q1).order_by('price')[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_session_list_pagination_filter_start_time(self):
        url = reverse('session-list')
        data = {'start_time': True}
        response = self.client.get(url, data=data)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date(),
               start_date__lte=timezone.now().date())
        sessions = Session.objects.filter(q1).order_by('start_time')[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_session_tomorrow_list_pagination_filter_start_time(self):
        url = reverse('session-tomorrow')
        data = {'start_time': True}
        response = self.client.get(url, data=data)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date() + timedelta(days=1),
               start_date__lte=timezone.now().date() + timedelta(days=1))
        sessions = Session.objects.filter(q1).order_by('start_time')[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_session_list_pagination_filter_price_and_start_time(self):
        url = reverse('session-list')
        data = {'price': True, 'start_time': True}
        response = self.client.get(url, data=data)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date(),
               start_date__lte=timezone.now().date())
        sessions = Session.objects.filter(q1).order_by('price', 'start_time')[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_session_tomorrow_list_pagination_filter_price_and_start_time(self):
        url = reverse('session-tomorrow')
        data = {'price': True, 'start_time': True}
        response = self.client.get(url, data=data)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date() + timedelta(days=1),
               start_date__lte=timezone.now().date() + timedelta(days=1))
        sessions = Session.objects.filter(q1).order_by('price', 'start_time')[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_session_list_pagination_filter_hall(self):
        url = reverse('session-list')
        data = {'hall': 1}
        response = self.client.get(url, data=data)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date(),
               start_date__lte=timezone.now().date())
        q2 = Q(hall=data['hall'])
        sessions = Session.objects.filter(q1 & q2)[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_session_tomorrow_list_pagination_filter_hall(self):
        url = reverse('session-tomorrow')
        data = {'hall': 1}
        response = self.client.get(url, data=data)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date() + timedelta(days=1),
               start_date__lte=timezone.now().date() + timedelta(days=1))
        q2 = Q(hall=data['hall'])
        sessions = Session.objects.filter(q1 & q2)[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data) 

    def test_session_list_pagination_filter_time(self):
        url = reverse('session-list')
        data = {'time': '12:00-15:25'}
        response = self.client.get(url, data=data)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date(),
               start_date__lte=timezone.now().date())
        time_list = data['time'].split('-')
        start = datetime.strptime(time_list[0], '%H:%M').time()
        end = datetime.strptime(time_list[1], '%H:%M').time()
        q3 = Q(start_time__gte=start, end_time__lte=end)
        sessions = Session.objects.filter(q1 & q3)[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_session_tomorrow_list_pagination_filter_time(self):
        url = reverse('session-tomorrow')
        data = {'time': '12:00-15:25'}
        response = self.client.get(url, data=data)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date() + timedelta(days=1),
               start_date__lte=timezone.now().date() + timedelta(days=1))
        time_list = data['time'].split('-')
        start = datetime.strptime(time_list[0], '%H:%M').time()
        end = datetime.strptime(time_list[1], '%H:%M').time()
        q3 = Q(start_time__gte=start, end_time__lte=end)
        sessions = Session.objects.filter(q1 & q3)[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_session_list_pagination_filter_hall_and_time(self):
        url = reverse('session-list')
        data = {'hall': 1, 'time': '12:00-15:25'}
        response = self.client.get(url, data=data)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date(),
               start_date__lte=timezone.now().date())
        q2 = Q(hall=data['hall'])
        time_list = data['time'].split('-')
        start = datetime.strptime(time_list[0], '%H:%M').time()
        end = datetime.strptime(time_list[1], '%H:%M').time()
        q3 = Q(start_time__gte=start, end_time__lte=end)
        sessions = Session.objects.filter(q1 & q2 & q3)[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_session_tomorrow_list_pagination_filter_hall_and_time(self):
        url = reverse('session-tomorrow')
        data = {'hall': 1, 'time': '12:00-15:25'}
        response = self.client.get(url, data=data)
        q1 = Q(status=True,
               end_date__gte=timezone.now().date() + timedelta(days=1),
               start_date__lte=timezone.now().date() + timedelta(days=1))
        q2 = Q(hall=data['hall'])
        time_list = data['time'].split('-')
        start = datetime.strptime(time_list[0], '%H:%M').time()
        end = datetime.strptime(time_list[1], '%H:%M').time()
        q3 = Q(start_time__gte=start, end_time__lte=end)
        sessions = Session.objects.filter(q1 & q2 & q3)[:3].annotate(total=Sum('session_tickets__quantity'))
        serializer = SessionCreateSerializer(sessions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_session_post_no_login(self):
        self.client.logout()
        url = reverse('session-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_session_post_no_superuser(self):
        url = reverse('session-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_session_post_succes(self):
        self.user.is_staff = True
        self.user.save()
        url = reverse('session-list')
        data = {
            'hall': self.hall.pk,
            'start_time': time(15, 00, 00),
            'end_time': time(16, 00, 00),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=5)).date(),
            'price': 100
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_session_post_failure(self):
        self.user.is_staff = True
        self.user.save()
        url = reverse('session-list')
        data = {
            'hall': self.hall.pk,
            'start_time': time(8, 00, 00),
            'end_time': time(16, 00, 00),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=5)).date(),
            'price': 100
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.data['non_field_errors'], ['Зал в это время занят'])

    def test_session_put_no_login(self):
        self.client.logout()
        url = reverse('session-detail', args=[self.session.pk])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_session_put_no_superuser(self):
        url = reverse('session-detail', args=[self.session.pk])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_session_put_succes(self):
        self.user.is_staff = True
        self.user.save()
        url = reverse('session-detail', args=[self.session.pk])
        data = {
            'hall': self.hall.pk,
            'start_time': time(15, 00, 00),
            'end_time': time(16, 00, 00),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=5)).date(),
            'price': 1000
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_session_put_failure(self):
        self.user.is_staff = True
        self.user.save()
        url = reverse('session-detail', args=[self.session.pk])
        data = {
            'hall': self.hall.pk,
            'start_time': time(10, 00, 00),
            'end_time': time(16, 00, 00),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=5)).date(),
            'price': 1000
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.data['non_field_errors'], ['Зал в это время занят'])

    def test_session_put_failure_busy(self):
        self.user.is_staff = True
        self.user.save()
        TicketFactory(session=self.session)
        url = reverse('session-detail', args=[self.session.pk])
        data = {
            'hall': self.hall.pk,
            'start_time': time(15, 00, 00),
            'end_time': time(16, 00, 00),
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=5)).date(),
            'price': 1000
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(response.data['detail'], ['You cannot change the session for which the ticket was purchased'])

    def test_session_patch_succes(self):
        self.user.is_staff = True
        self.user.save()
        url = reverse('session-detail', args=[self.session.pk])
        data = {
            'start_time': time(15, 00, 00),
            'end_time': time(16, 00, 00),
            'price': 1000
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_session_patch_failure(self):
        self.user.is_staff = True
        self.user.save()
        url = reverse('session-detail', args=[self.session.pk])
        data = {
            'start_time': time(10, 00, 00),
            'end_time': time(16, 00, 00),
            'price': 1000
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.data['non_field_errors'], ['Зал в это время занят'])

    def test_session_patch_failure_busy(self):
        self.user.is_staff = True
        self.user.save()
        TicketFactory(session=self.session)
        url = reverse('session-detail', args=[self.session.pk])
        data = {
            'start_time': time(15, 00, 00),
            'end_time': time(16, 00, 00),
            'price': 1000
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(response.data['detail'], ['You cannot change the session for which the ticket was purchased'])

class TicketViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.hall = CinemaHallFactory()
        self.session = SessionFactory(hall=self.hall, start_time=time(2, 10, 00), end_time=time(3, 00, 00))
        self.ticket = TicketFactory(session=self.session, customer=self.user)
        TicketFactory(session=self.session, customer=self.user)
        TicketFactory(session=self.session, customer=self.user)
        TicketFactory(session=self.session, customer=self.user)

    def test_ticket_list_pagination(self):
        url = reverse('ticket-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ticket_post_succes(self):
        url = reverse('ticket-list')
        data = {'session': self.session.pk, 'quantity': 2}
        response = self.client.post(url, data=data)
        suma = self.session.price * data['quantity']
        self.assertEqual(response.data['total_price'], suma)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ticket_post_failure(self):
        url = reverse('ticket-list')
        data = {'session': self.session.pk, 'quantity': 40}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
