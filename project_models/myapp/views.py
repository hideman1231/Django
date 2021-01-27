from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import MyLoginForm, MyRegisterForm, ContentCommentsForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class CommentView(ListView):
	model = Comment
	form_class = ContentCommentsForm
	template_name = 'index.html'
	context_object_name = 'comment_list'
	def get_queryset(self):
		form = self.form_class(self.request.GET)
		if form.is_valid():
			return Comment.objects.filter(name__icontains=form.cleaned_data['content'])
		return Comment.objects.all()


class MyLoginView(LoginView):
	template_name = 'req.html'
	http_method_names = ['get', 'post']
	form_class = MyLoginForm
	success_url = '/'
	def get_success_url(self):
		return self.success_url


class MyRegisterView(CreateView):
	model = User
	form_class = MyRegisterForm
	template_name = 'register.html'
	success_url = '/'


class LogoutUserView(LogoutView):
	next_page = '/'










	




