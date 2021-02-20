from rest_framework import serializers
from myshop.models import CustomUser, Product, Purchase, Author, Book, PurchaseReturn
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.validators import UniqueTogetherValidator
from django.utils import timezone
from datetime import timedelta


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'wallet']
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity']


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ['product', 'quantity']

    def validate(self, data):
        if data['product'].quantity < data['quantity']:
            raise serializers.ValidationError('Товара не хватает') 
        elif data['product'].price * data['quantity'] > self.context['request'].user.wallet:
            raise serializers.ValidationError('У вас не хватает зелени')
        return data



class PurchaseReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseReturn
        fields = ['purchase', 'return_time']
        read_only = ('return_time', )


    def validate_purchase(self, value):
        if value.buyer == self.context['request'].user:
            if PurchaseReturn.objects.filter(purchase=value):
                raise serializers.ValidationError('Чувак ты уже отправлял это товар на возврат')
            elif value.purchase_time + timedelta(minutes=3) < timezone.now():
                raise serializers.ValidationError('Время вышло, раньше думать нужно)')
        else:
            raise serializers.ValidationError('Это не твоя покупка!')
        return value


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['name', 'age']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['author', 'title', 'page']
        validators = [
            UniqueTogetherValidator(
                queryset=Book.objects.all(),
                fields=['title']
            )
        ]

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        title_data = validated_data.pop('title')
        title = title_data + '!'
        author, created = Author.objects.get_or_create(**author_data)
        return Book.objects.create(author=author, title=title, **validated_data)


class AuthorBookSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['books']
