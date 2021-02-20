from rest_framework import viewsets
from myshop.models import (Author, Book, CustomUser,
                           Product, Purchase, PurchaseReturn)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from myshop.api.serializers import (AuthorSerializer, BookSerializer, AuthorBookSerializer,
                                    CustomUserSerializer, PurchaseSerializer, PurchaseReturnSerializer)
from rest_framework.views import APIView
from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# class CustomTokenAuthentication(TokenAuthentication):
#     pass
    # model = CustomToken

    # def authenticate_credentials(self, key):
    #     user, token = super().authenticate_credentials(key)
    #     if timezone.now() > token.created + timedelta(minutes=10):
    #         raise exceptions.AuthenticationFailed('Токену габела, 10 мин прошло')
    #     return user, token


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.request.data['product'])
        suma = self.request.data['quantity'] * product.price
        user = self.request.user
        user.wallet -= suma
        user.save()
        product.quantity -= self.request.data['quantity']
        product.save()
        serializer.save(buyer=user)


class PurchaseReturnViewSet(viewsets.ModelViewSet):
    queryset = PurchaseReturn.objects.all()
    serializer_class = PurchaseReturnSerializer

    def perform_create(self, serializer):
        user = self.request.user
        purchase = Purchase.objects.get(id=self.request.data['purchase'])
        product = Product.objects.get(id=purchase.product.id)
        suma = product.price * purchase.quantity
        user.wallet += suma
        product.quantity += purchase.quantity
        user.save()
        product.save()
        serializer.save()
        purchase.delete()


class ExampleView(APIView):

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
            'token_time': str(request.auth.created < timezone.now() + timedelta(minutes=10))
        }
        return Response(content)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        name_param = self.request.query_params.get('name')
        if name_param:
            return Author.objects.filter(name=name_param)
        return Author.objects.all()

    @action(detail=True, methods=['get'])
    def get_books(self, request, pk):
        author = self.get_object()
        serializer = AuthorBookSerializer(author)
        return Response({'books': serializer.data['books']})


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        age_param = self.request.query_params.get('age')
        if age_param:
            return Book.objects.filter(author__age__gt=age_param)
        return Book.objects.filter(author__age__gt=30)
