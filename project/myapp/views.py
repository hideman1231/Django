from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse('index')

def articles(request):
	return HttpResponse('articles')

def articles_arhive(request):
	return HttpResponse('articles_arhive')

def users(request):
	return HttpResponse('users')

def article(request):
	return HttpResponse('article')

def article_num(request, article_number):
	return HttpResponse(article_number)

def article_num_arhive(request, article_number):
	return HttpResponse('{} arhive'.format(article_number))

def article_num_slug(request, article_number, slug_text):
	return HttpResponse('{} {}'.format(article_number, slug_text))

def users_num(request, user_number):
	return HttpResponse('{} - user'.format(user_number))

def phone(request):
	return HttpResponse('phone')

def symbol(request):
	return HttpResponse('symbol')