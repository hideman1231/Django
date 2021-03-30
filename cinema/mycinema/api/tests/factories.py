import factory
from mycinema.models import MyUser, CinemaHall, Session, Ticket
from faker import Faker
from django.utils import timezone
from datetime import timedelta


fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = MyUser

    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', '1')


class CinemaHallFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CinemaHall

    name = fake.word()
    size = 20


class SessionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Session

    hall = factory.SubFactory(CinemaHallFactory)
    start_time = fake.time()
    end_time = fake.time()
    start_date = timezone.now().date()
    end_date = (timezone.now() + timedelta(days=5)).date()
    price = 100

    if start_time > end_time:
        start_time, end_time = end_time, start_time


class TicketFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Ticket

    customer = factory.SubFactory(UserFactory)
    session = factory.SubFactory(SessionFactory)
    quantity = 1
