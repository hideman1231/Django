from django.contrib.auth.forms import UserCreationForm
from mycinema.models import MyUser, CinemaHall, Session, Ticket
from django import forms
from django.utils import timezone

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2')


class CreateCinemaHallForm(forms.ModelForm):
    class Meta:
        model = CinemaHall
        fields = '__all__'


class CreateSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('hall', 'start_time', 'end_time', 'price')
        widgets = {
            'start_time': forms.DateInput(attrs={'type': 'date'}),
            'end_time': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hall = cleaned_data['hall']
        session = CinemaHall.objects.get(id=hall.pk).sessions.last()
        print(session)
        start_time = cleaned_data['start_time']
        end_time = cleaned_data['end_time']
        if start_time > end_time:
            self.add_error('start_time', 'Не верная дата')
        if session is not None:
            if start_time <= session.end_time:
                self.add_error('hall', 'Зал уже занят')


class QuantityTicketForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = Ticket
        fields = ('quantity', )


