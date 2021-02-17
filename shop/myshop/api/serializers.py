from rest_framework import serializers
from myshop.models import CustomUser, Product, Purchase, Author, Book
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.validators import UniqueTogetherValidator


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
                queryset = Book.objects.all(),
                fields = ['title']
            )
        ]

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        title_data = validated_data.pop('title')
        title = title_data + '!'
        if Author.objects.filter(name=author_data['name'], age=author_data['age']):
            author = Author.objects.get(**author_data)
        else:
            author = Author.objects.create(**author_data)
        return Book.objects.create(author=author, title=title, **validated_data)



class AuthorBookSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['books']


