from django.urls import path

from mycinema.views import (SessionListView, UserLoginView, UserRegisterView, 
                            UserLogoutView, CreateCinemaHallView, CreateSessionView,
                            )

urlpatterns = [
    path('', SessionListView.as_view(), name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('create-cinema-hall/', CreateCinemaHallView.as_view(), name='create_cinema_hall'),
    path('create-session/', CreateSessionView.as_view(), name='create_session')
]
