from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from mycinema.models import MyUser, CinemaHall, Session, Ticket
from mycinema.forms import (MyUserCreationForm, CreateCinemaHallForm, CreateSessionForm,
                            QuantityTicketForm, UpdateSessionForm, FilterForm)
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import timedelta
from django.contrib.auth.mixins import UserPassesTestMixin


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
    extra_context = {'quantity':QuantityTicketForm}
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['filter'] = FilterForm
        return context

    def get_queryset(self):
        if self.request.GET.get('filter_price'):
            return super().get_queryset().filter(status=True, end_date__gte=timezone.now().date(), start_date__lte=timezone.now().date()).order_by('price')
        elif self.request.GET.get('filter_start_time'):
            return super().get_queryset().filter(status=True, end_date__gte=timezone.now().date(), start_date__lte=timezone.now().date()).order_by('start_time')
        return super().get_queryset().filter(status=True, end_date__gte=timezone.now().date(), start_date__lte=timezone.now().date())


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


class CreateTicketView(CreateView):
    model = Ticket
    form_class = QuantityTicketForm
    success_url = reverse_lazy('index')
    template_name = 'index.html'

    def form_valid(self, form):
        quantity = int(self.request.POST['quantity'])
        session = Session.objects.get(id=self.request.POST['session'])
        hall = session.hall
        customer = self.request.user
        free_places = hall.size - session.session_tickets.count()
        if free_places - quantity < 0:
            messages.error(self.request, f'Мест не хватает! Свободных мест: {free_places}')
            return HttpResponseRedirect(self.success_url)
        for i in range(quantity):
            Ticket.objects.create(customer=customer, session=session)
        customer.total_price += session.price 
        customer.save()
        return HttpResponseRedirect(self.success_url)

class UserPurchaseListView(ListView):
    template_name = 'purchases.html'
    model = Ticket
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)


class UpdateCinemaHallView(UserPassesTestMixin, UpdateView):
    model = CinemaHall
    success_url = reverse_lazy('index')
    form_class = CreateCinemaHallForm
    template_name = 'update_cinema_hall.html'

    def test_func(self):
        sessions = self.get_object().sessions.filter(status=True)
        if sessions:
            for session in sessions:
                if session.session_tickets.first():
                    return False
        return True


class UpdateSessionView(UserPassesTestMixin, UpdateView):
    model = Session
    success_url = reverse_lazy('index')
    form_class = UpdateSessionForm
    template_name = 'update_session.html'

    def test_func(self):
        session = self.get_object()
        if session.session_tickets.first():
            return False
        return True


class SessionForTomorrowListView(ListView):
    model = Session
    template_name = 'session_for_tomorrow.html'
    extra_context = {'quantity': QuantityTicketForm}
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['filter'] = FilterForm
        return context

    def get_queryset(self):
        if self.request.GET.get('filter_price'):
            return super().get_queryset().filter(status=True, end_date__gte=timezone.now().date() + timedelta(days=1), start_date__lte=timezone.now().date() + timedelta(days=1)).order_by('price')
        elif self.request.GET.get('filter_start_time'):
            return super().get_queryset().filter(status=True, end_date__gte=timezone.now().date() + timedelta(days=1), start_date__lte=timezone.now().date() + timedelta(days=1)).order_by('start_time')
        return super().get_queryset().filter(status=True, end_date__gte=timezone.now().date() + timedelta(days=1), start_date__lte=timezone.now().date() + timedelta(days=1))