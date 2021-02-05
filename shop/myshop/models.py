from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
	wallet = models.PositiveIntegerField(default=1000)


class Product(models.Model):
	name = models.CharField(max_length=50)
	photo = models.ImageField(null=True)
	description = models.TextField()
	price = models.PositiveIntegerField()
	quantity = models.PositiveSmallIntegerField()

	def __str__(self):
		return self.name


class Purchase(models.Model):
	buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='buyers')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='products')
	quantity = models.PositiveSmallIntegerField()
	purchase_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-purchase_time']

	def __str__(self):
		return f'{self.product.name} | {self.buyer.username} | {self.quantity} | {self.purchase_time}'


class PurchaseReturn(models.Model):
	purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, verbose_name='purchases')
	return_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-return_time']

	def __str__(self):
		return f'{self.purchase} | {self.return_time}'









