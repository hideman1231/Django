from django.urls import path

from .views import my_comments, create_comment, MyLoginView, MyRegisterView, LogoutUserView, UpdateUserView


urlpatterns = [
	path('', my_comments, name='index'),
	path('create_comment/', create_comment, name='create_comment'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('register/', MyRegisterView.as_view(), name='register'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('changepassword/', UpdateUserView.as_view(), name='changepas'),


]