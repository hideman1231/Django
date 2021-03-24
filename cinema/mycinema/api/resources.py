from mycinema.models import MyUser, CinemaHall, Session, Ticket, MyToken
from mycinema.api.serializers import (MyUserSerializer, CinemaHallSerializer, SessionCreateSerializer,
                                    SessionUpdateSerializer, TicketSerializer)
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from datetime import timedelta
from django.utils import timezone
from .permissions import CustomSessionUpdatePermisson, CustomCinemaHallUpdatePermisson


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    http_method_names = ['get', 'post']
    # permission_classes = [permissions.IsAdminUser]


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    permission_classes = [CustomCinemaHallUpdatePermisson]


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionCreateSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    permission_classes = [permissions.IsAdminUser, CustomSessionUpdatePermisson]

    def get_serializer_class(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            return SessionUpdateSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.request.user.is_authenticated:
            price = self.request.query_params.get('price')
            start_time = self.request.query_params.get('price')
            if price and start_time:
                return Session.objects.filter(status=True).order_by('price', 'start_time')
            elif price:
                return Session.objects.filter(status=True).order_by('price')
            elif start_time:
                return Session.objects.filter(status=True).order_by('start_time')
        return self.queryset


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        session = Session.objects.get(id=self.request.data['session'])
        quantity = self.request.data['quantity']
        user.total_price += session.price * quantity
        user.save()
        serializer.save(customer=user)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = MyToken.objects.get_or_create(user=user)
        return Response({'token': token.key, 'time_to_die': '{}'.format(token.time_to_die + timedelta(minutes=5) if not user.is_superuser else None)})


# class UserRegisterApiView()