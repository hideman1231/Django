from django.urls import path, re_path
from .views import index, articles, articles_arhive, users, article, article_num, article_num_arhive, article_num_slug, users_num, phone, symbol

urlpatterns = [
    path('', index, name='index'),
    path('articles/', articles, name='articles'),
    path('articles/arhive/', articles_arhive, name='articles_arhive'),\
    path('users/', users, name='users'),
    path('article/', article, name='article'),
    path('article/<int:article_number>/', article_num, name='article_num'),
    path('article/<int:article_number>/arhive/', article_num_arhive, name='article_num_arhive'),
    path('article/<int:article_number>/<slug:slug_text>/', article_num_slug, name='article_num'),
    path('users/<int:user_number>', users_num, name='users_num'),
	re_path(r'0(?:[69][3876]|9[9124]|50|39)\d{7}/', phone, name='phone'),
    re_path(r'(?:\d|[a-f]){4}-(?:\d|[a-f]){6}/', symbol, name='symbol'),
]
