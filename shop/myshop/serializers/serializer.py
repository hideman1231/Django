from rest_framework import serializers
from myshop.models import CustomUser, Product, Purchase
from django.contrib.auth.hashers import make_password


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password','wallet']
        write_only_fields = ('password',)

    # def create(self, validated_data):
    #     user = CustomUser(
    #         username = validated_data['username'],
    #         wallet = validated_data['wallet'],
    #         password = make_password(validated_data['password']),
    #         )
    #     user.save()
    #     return user

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','description','price','quantity']


class PurchaseSerializer(serializers.ModelSerializer):
    buyer = CustomUserSerializer()
    product = ProductSerializer()

    class Meta:
        model = Purchase
        fields = ['buyer','product','quantity']