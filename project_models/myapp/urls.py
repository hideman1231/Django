from django.urls import path

from .views import CommentView, MyLoginView, MyRegisterView, LogoutUserView


urlpatterns = [
	path('', CommentView.as_view(), name='index'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('register/', MyRegisterView.as_view(), name='register'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]