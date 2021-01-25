from django.urls import path

from .views import index, articles, createArticle, updateArticle, deleteArticle


urlpatterns = [
    path('', index, name='index'),
    path('article/<int:article_id>/', articles, name='articles'),
    path('article/create/', createArticle, name='createArticle'),
    path('article/update/<int:article_id>', updateArticle, name='updateArticle'),
    path('article/delete/<int:article_id>', deleteArticle, name='deleteArticle'),
]