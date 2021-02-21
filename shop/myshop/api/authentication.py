from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.utils import timezone
from datetime import timedelta
import pdb


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid Token")
        if timezone.now() > token.created + timedelta(minutes=10):
            user = token.user
            token.delete()
            token = Token.objects.create(user=user)
        return token.user, token
