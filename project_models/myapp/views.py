from django.shortcuts import render
from .models import Article, Comment
from .forms import ArticleForm
from django.http import HttpResponseRedirect


def index(request):
	form = Article.objects.all()
	return render(request, 'index.html', {'form': form})

def create(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/')
	else:
		form = ArticleForm()
	print(form.is_valid())
	return render(request, 'create.html', {'form': form})
