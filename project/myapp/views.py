import random
import string

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	return render(request, 'index.html')


def articles(request):
	return render(request, 'articles.html')


def articles_arhive(request):
	return render(request, 'articles_arhive.html')


def users(request):
	return render(request, 'users.html')


def article(request):
	return HttpResponse('article')


def article_num(request, article_number):
	data = {
		'article_number':article_number,
	}
	return render(request, 'num.html', data)


def article_num_arhive(request, article_number):
	return HttpResponse('{} arhive'.format(article_number))


def article_num_slug(request, article_number, slug_text):
	data = {
		'article_number':article_number,
		'slug':slug_text,
	}
	return render(request, 'num.html', data)


def users_num(request, user_number):
	return HttpResponse('{} - user'.format(user_number))


def phone(request):
	return HttpResponse('phone')


def symbol(request):
	return HttpResponse('symbol')