from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import ArticleForm


def index(request):
	form = Article.objects.all()
	return render(request, 'index.html', {'form': form})


def articles(request, article_id):
	form = Article.objects.get(id=article_id)
	comments = form.article.all()
	return render(request, 'articles.html', {'form': form, 'comments':comments})


def createArticle(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form = ArticleForm()
	return render(request, 'create.html', {'form': form})


def updateArticle(request, article_id):
	article = Article.objects.get(id=article_id)
	form = ArticleForm(instance=article)

	if request.method == 'POST':
		form = ArticleForm(request.POST, instance=article)
		if form.is_valid():
			form.save()
			return redirect('/')

	return render(request, 'update.html', {'form': form})


def deleteArticle(request, article_id):
	article = Article.objects.get(id=article_id)

	if request.method == 'POST':
		article.delete()
		return redirect('/')
	return render(request, 'delete.html', {'form': article})



	




