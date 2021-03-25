from mycinema.models import MyUser, CinemaHall, Session, Ticket, MyToken
from mycinema.api.serializers import (MyUserRegisterSerializer, CinemaHallSerializer, SessionCreateSerializer,
                                    SessionUpdateSerializer, TicketSerializer)
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions, generics, pagination
from rest_framework.authtoken.views import ObtainAuthToken
from datetime import timedelta
from django.utils import timezone
from .permissions import CustomSessionUpdatePermisson, CustomCinemaHallUpdatePermisson
from django.db.models import Sum


class MyPageNumberPagination(pagination.PageNumberPagination):
    page_size = 3

# class CinemaHallViewSet(viewsets.ModelViewSet):
#     queryset = CinemaHall.objects.all()
#     serializer_class = CinemaHallSerializer
#     http_method_names = ['get', 'post', 'put', 'patch']
#     permission_classes = [CustomCinemaHallUpdatePermisson]


# class SessionViewSet(viewsets.ModelViewSet):
#     queryset = Session.objects.all()
#     serializer_class = SessionCreateSerializer
#     http_method_names = ['get', 'post', 'put', 'patch']
#     permission_classes = [permissions.IsAdminUser, CustomSessionUpdatePermisson]

#     def get_serializer_class(self):
#         if self.request.method == 'PATCH' or self.request.method == 'PUT':
#             return SessionUpdateSerializer
#         return self.serializer_class

#     def get_queryset(self):
#         if self.request.user.is_authenticated:
#             price = self.request.query_params.get('price')
#             start_time = self.request.query_params.get('price')
#             if price and start_time:
#                 return Session.objects.filter(status=True).order_by('price', 'start_time')
#             elif price:
#                 return Session.objects.filter(status=True).order_by('price')
#             elif start_time:
#                 return Session.objects.filter(status=True).order_by('start_time')
#         return self.queryset


# class TicketViewSet(viewsets.ModelViewSet):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#     http_method_names = ['get', 'post']
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         user = self.request.user
#         session = Session.objects.get(id=self.request.data['session'])
#         quantity = self.request.data['quantity']
#         user.total_price += session.price * quantity
#         user.save()
#         serializer.save(customer=user)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = MyToken.objects.get_or_create(user=user)
        return Response({'token': token.key, 'time_to_die': '{}'.format(token.time_to_die + timedelta(minutes=5) if not user.is_superuser else None)})


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserRegisterSerializer


class SessionListAPIView(generics.ListAPIView):
    serializer_class = SessionCreateSerializer
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            price = self.request.query_params.get('price')
            start_time = self.request.query_params.get('start_time')
            if price and start_time:
                return Session.objects.filter(
                    status=True,
                    end_date__gte=timezone.now().date(),
                    start_date__lte=timezone.now().date()).order_by('price', 'start_time').annotate(total=Sum('session_tickets__quantity'))
            elif price:
                return Session.objects.filter(
                    status=True,
                    end_date__gte=timezone.now().date(),
                    start_date__lte=timezone.now().date()).order_by('price').annotate(total=Sum('session_tickets__quantity'))
            elif start_time:
                return Session.objects.filter(
                    status=True,
                    end_date__gte=timezone.now().date(),
                    start_date__lte=timezone.now().date()).order_by('start_time').annotate(total=Sum('session_tickets__quantity'))
        return Session.objects.filter(
            status=True,
            end_date__gte=timezone.now().date(),
            start_date__lte=timezone.now().date()).annotate(total=Sum('session_tickets__quantity'))


class CreateCinemaHallAPIView(generics.CreateAPIView):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    permission_classes = [permissions.IsAdminUser]


class CreateSessionAPIView(generics.CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class CreateTicketAPIView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        session = Session.objects.get(id=self.request.data['session'])
        quantity = self.request.data['quantity']
        user.total_price += session.price * quantity
        user.save()
        serializer.save(customer=user)


class UserPurchaseListAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        return Ticket.objects.filter(customer=self.request.user)


class UpdateCinemaHallAPIView(generics.UpdateAPIView):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    permission_classes = [permissions.IsAdminUser, CustomCinemaHallUpdatePermisson]


class UpdateSessionAPIView(generics.UpdateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionUpdateSerializer
    permission_classes = [permissions.IsAdminUser, CustomSessionUpdatePermisson]


class SessionForTomorrowListAPIView(generics.ListAPIView):
    serializer_class = SessionCreateSerializer
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            price = self.request.query_params.get('price')
            start_time = self.request.query_params.get('start_time')
            hall = self.request.query_params.get('hall')
            if price and start_time:
                return Session.objects.filter(
                    status=True,
                    end_date__gte=timezone.now().date() + timedelta(days=1),
                    start_date__lte=timezone.now().date() + timedelta(days=1)).order_by('price', 'start_time').annotate(total=Sum('session_tickets__quantity'))
            elif price:
                return Session.objects.filter(status=True,
                end_date__gte=timezone.now().date() + timedelta(days=1),
                start_date__lte=timezone.now().date() + timedelta(days=1)).order_by('price').annotate(total=Sum('session_tickets__quantity'))
            elif start_time:
                return Session.objects.filter(
                    status=True,
                    end_date__gte=timezone.now().date() + timedelta(days=1),
                    start_date__lte=timezone.now().date() + timedelta(days=1)).order_by('start_time').annotate(total=Sum('session_tickets__quantity'))
        return Session.objects.filter(
            status=True,
            hall=hall,
            end_date__gte=timezone.now().date() + timedelta(days=1),
            start_date__lte=timezone.now().date() + timedelta(days=1)).annotate(total=Sum('session_tickets__quantity'))

