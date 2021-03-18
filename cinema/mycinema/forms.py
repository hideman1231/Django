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
        fields = ('hall', 'start_time', 'end_time', 'start_date', 'end_date', 'price')
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hall = cleaned_data['hall']
        start_time = cleaned_data['start_time']
        end_time = cleaned_data['end_time']
        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']
        if start_time >= end_time:
            self.add_error('start_time', 'Начало не может быть больше конца')
        sessions_that_overlap = hall.sessions.filter(status=True, end_date__gte=start_date, start_date__lte=end_date)
        if sessions_that_overlap:
            if sessions_that_overlap.filter(end_time__gte=start_time, start_time__lte=end_time):
                self.add_error('hall', 'Зал в это время занят')


class QuantityTicketForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = Ticket
        fields = ('quantity', )


class UpdateSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('hall', 'start_time', 'end_time', 'start_date', 'end_date', 'price')
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date':forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        curent_session = self.instance
        cleaned_data = super().clean()
        hall = cleaned_data['hall']
        start_time = cleaned_data['start_time']
        end_time = cleaned_data['end_time']
        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']
        if start_time >= end_time:
            self.add_error('start_time', 'Начало не может быть больше конца')
        sessions_that_overlap = hall.sessions.filter(status=True, end_date__gte=start_date, start_date__lte=end_date).exclude(id=curent_session.pk)
        if sessions_that_overlap:
            if sessions_that_overlap.filter(status=True, end_time__gte=start_time, start_time__lte=end_time):
                self.add_error('hall', 'Зал в это время занят')


class FilterForm(forms.Form):
    filter_price = forms.BooleanField(label='Фильтрация по ценам', required=False)
    filter_start_time = forms.BooleanField(label='Фильтрация по началу', required=False)