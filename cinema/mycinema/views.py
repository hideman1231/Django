from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView
from mycinema.models import MyUser, CinemaHall, Session, Ticket
from mycinema.forms import MyUserCreationForm, CreateCinemaHallForm, CreateSessionForm
from django.utils import timezone
from django.urls import reverse_lazy


class UserLoginView(LoginView):
    success_url = reverse_lazy('index')
    template_name = 'login.html'

    def get_success_url(self):
        return self.success_url 

    def form_valid(self, form):
        self.request.session['time_action'] = str(timezone.now())
        return super().form_valid(form=form)


class UserRegisterView(CreateView):
    model = MyUser
    form_class = MyUserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'register.html'  


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class SessionListView(ListView):
    model = Session
    template_name = 'index.html'
    context_object_name = 'sessions'


class CreateCinemaHallView(CreateView):
    model = CinemaHall
    form_class = CreateCinemaHallForm
    success_url = reverse_lazy('index')
    template_name = 'create_cinema_hall.html'


class CreateSessionView(CreateView):
    model = Session
    form_class = CreateSessionForm
    success_url = reverse_lazy('index')
    template_name = 'create_session.html'
