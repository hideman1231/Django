from django.contrib.auth.forms import UserCreationForm
from mycinema.models import MyUser, CinemaHall, Session, Ticket
from django import forms

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

    def clean_hall(self):
        data = self.cleaned_data.get('hall')
        if data in [s.hall for s in Session.objects.all()]:
            return forms.ValidationError('Этот зал уже занят')
        return data

