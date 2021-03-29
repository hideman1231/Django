from django.urls import path, include
from mycinema.views import (SessionListView, UserLoginView, UserRegisterView, 
                            UserLogoutView, CreateCinemaHallView, CreateSessionView,
                            CreateTicketView, UserPurchaseListView, UpdateCinemaHallView,
                            UpdateSessionView, SessionForTomorrowListView)
# from mycinema.api.resources import (UserRegisterAPIView, CustomAuthToken, SessionListAPIView,
#                                     CreateCinemaHallAPIView, CreateSessionAPIView, CreateTicketAPIView,
#                                     UserPurchaseListAPIView, UpdateCinemaHallAPIView, UpdateSessionAPIView,
#                                     SessionForTomorrowListAPIView)
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from mycinema.api.resources import (UserRegisterAPIView, CinemaHallViewSet, SessionViewSet, 
                                    TicketViewSet, CustomAuthToken)


router = routers.SimpleRouter()
router.register(r'cinema-halls', CinemaHallViewSet, basename='cinema-halls')
router.register(r'sessions', SessionViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    # Django

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

    # Django rest_framework

    path('api/', include(router.urls)),
    path('api/token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('api/register/', UserRegisterAPIView.as_view(), name='api_register'),


    # path('api/token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    # path('api/register/', UserRegisterAPIView.as_view(), name='api_register'),
    # path('api/sessions/', SessionListAPIView.as_view(), name='api_sessions'),
    # path('api/create/cinema-hall/', CreateCinemaHallAPIView.as_view(), name='api_create_cinema_hall'),
    # path('api/create/session/', CreateSessionAPIView.as_view(), name='api_create_session'),
    # path('api/create/ticket/', CreateTicketAPIView.as_view(), name='api_create_ticket'),
    # path('api/purchases/', UserPurchaseListAPIView.as_view(), name='api_purchases'),
    # path('api/update/cinema-hall/<int:pk>/', UpdateCinemaHallAPIView.as_view(), name='api_update_cinema_hall'),
    # path('api/update/session/<int:pk>/', UpdateSessionAPIView.as_view(), name='api_update_session'),
    # path('api/sessions/tomorrow/', SessionForTomorrowListAPIView.as_view(), name='api_sessions_for_tomorrow'),
]
