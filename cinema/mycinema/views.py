from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, DetailView
from mycinema.models import MyUser, CinemaHall, Session, Ticket
from mycinema.forms import (MyUserCreationForm, CreateCinemaHallForm, CreateSessionForm,
                            QuantityTicketForm)
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages


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

    def get_queryset(self):
        return super().get_queryset().filter(status=True)



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
    extra_context = {'free_places': 0}

    def form_valid(self, form):
        quantity = int(self.request.POST['quantity'])
        session = Session.objects.get(id=self.request.POST['session'])
        hall = session.hall
        customer = self.request.user
        free_places = hall.size - len(session.session_tickets.all())
        SessionListView.extra_context['free_places'] = free_places
        print(self.extra_context)
        print(SessionListView.extra_context)
        if free_places - quantity < 0:
            messages.error(self.request, f'Мест не хватает! Свободных мест: {free_places}')
            return HttpResponseRedirect(self.success_url)
        for i in range(quantity):
            Ticket.objects.create(customer=customer, session=session)
        customer.total_price += session.price 
        customer.save()
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        session = Session.objects.get(id=self.request.POST['session'])
        hall = session.hall
        free_places = hall.size - len(session.session_tickets.all())
        return super().get_context_data(free_places=free_places, **kwargs)


class UserPurchaseListView(ListView):
    template_name = 'purchases.html'
    model = Ticket
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)
