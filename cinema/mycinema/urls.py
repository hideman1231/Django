from django.urls import path

from mycinema.views import (SessionListView, UserLoginView, UserRegisterView, 
                            UserLogoutView, CreateCinemaHallView, CreateSessionView,
                            CreateTicketView, UserPurchaseListView, UpdateCinemaHallView,
                            UpdateSessionView, SessionForTomorrowListView)

urlpatterns = [
    path('', SessionListView.as_view(), name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('create/cinema-hall/', CreateCinemaHallView.as_view(), name='create_cinema_hall'),
    path('create/session/', CreateSessionView.as_view(), name='create_session'),
    path('create/ticket/', CreateTicketView.as_view(), name='create_ticket'),
    path('purchases/', UserPurchaseListView.as_view(), name='purchases'),
    path('update/cinema-hall/<int:pk>/', UpdateCinemaHallView.as_view(), name='update_cinema_hall'),
    path('update/session/<int:pk>/', UpdateSessionView.as_view(), name='update_session'),
    path('sessions/tomorrow/', SessionForTomorrowListView.as_view(), name='sessions_for_tomorrow'),
]
