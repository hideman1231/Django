from rest_framework import serializers
from myshop.models import CustomUser, Product, Purchase
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password','wallet']
        write_only_fields = ('password',)
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

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

    def create(self, validated_data):
        buyer_data = validated_data.pop('buyer')
        product_data = validated_data.pop('product')
        if CustomUser.objects.filter(username=buyer_data['username']):
            buyer = CustomUser.objects.get(**buyer_data)
        else:
            buyer = CustomUser(**buyer_data)
            buyer.set_password(buyer_data['password'])
            buyer.save()
        product, created  = Product.objects.get_or_create(**product_data)
        purchase = Purchase.objects.create(buyer=buyer, product=product, **validated_data)
        return purchase
