from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import CommentForm, MyLoginForm, MyRegisterForm, SearchCommentsForm, UpdateUserForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


def my_comments(request):
	com = ''
	if request.method == 'POST':
		form = SearchCommentsForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['my_comment']:
				com = Comment.objects.filter(content__icontains=form.cleaned_data['content'], author=request.user)
			else:
				com = Comment.objects.filter(content__icontains=form.cleaned_data['content'])
	else:
		form = SearchCommentsForm()
	return render(request, 'index.html', {'form': form, 'com': com})


def create_comment(request):
	if request.method == 'POST':
		try:
			article = Article.objects.get(content=request.POST['article_title'])
		except SomeModel.DoesNotExist:
			return ''
		author = request.user
		Comment.objects.create(article=article,author=request.user, content=request.POST['content'])
		return redirect('/')
	else:
		form = CommentForm()
	return render(request, 'create_comment.html', {'form':form})


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


class UpdateUserView(PasswordChangeView):
	form_class = UpdateUserForm
	template_name = 'updatelogin.html'
	success_url = '/'











	




