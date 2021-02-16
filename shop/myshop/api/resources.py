from myshop.api.serializers import AuthorSerializer, BookSerializer
from rest_framework import viewsets
from myshop.models import Author, Book


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        name_param = self.request.query_params.get('name')
        if name_param:
            return Author.objects.filter(name=name_param)
        return Author.objects.all()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        age_param = self.request.query_params.get('age') 
        if age_param:
            return Book.objects.filter(author__age__gt=age_param)
        return Book.objects.filter(author__age__gt=30)