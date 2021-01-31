from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import MyRegisterForm, CreateProductsForm, CreatePurchaseForm, PurchaseReturnForm
from .models import CustomUser, Product, Purchase, PurchaseReturn
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone


class LoginUserView(LoginView):
	success_url = '/'
	template_name = 'login.html'
	def get_success_url(self):
		return self.success_url


class LogoutUserView(LogoutView):
	next_page = '/'


class RegisterUserView(CreateView):
	model = CustomUser
	form_class = MyRegisterForm
	template_name = 'register.html'
	success_url = '/'


class ProductsView(ListView):
	model = Product
	template_name = 'index.html'
	extra_context = {'form_create_purchare':CreatePurchaseForm}


class CreateProductsView(CreateView):
	model = Product
	form_class = CreateProductsForm
	template_name = 'product_create.html'
	success_url = '/'


class ProductListView(ListView):
	model = Product
	template_name = 'product_list.html'


class UpdateProductView(UpdateView):
	model = Product
	template_name = 'product_update.html'
	success_url = '/'
	fields = '__all__'


class ProductReturnListView(ListView):
	model = PurchaseReturn
	template_name = 'product_return.html'


class PurchasesView(CreateView):
	model = Purchase
	form_class = CreatePurchaseForm
	template_name = 'purchase_create.html'
	success_url = '/'
	def form_valid(self, form):
		object = form.save(commit=False)
		object.buyer = self.request.user
		product = Product.objects.get(id=self.request.POST['product_pk'])
		object.product = product
		suma = object.quantity * product.price
		if self.request.user.wallet < suma:
			# form.add_error('quantity','Не хватает денег')
			# return super().form_invalid(form=form) Так не работает
			raise ValidationError('Не хватает денег')
		elif object.quantity > product.quantity:
			raise ValidationError('Не хватает товара')
		else:
			product.quantity = product.quantity - object.quantity
			product.save()
			user = CustomUser.objects.get(username=self.request.user)
			user.wallet -= suma
			user.save()
		return super().form_valid(form=form)


class PurchaseListView(ListView):
	model = Purchase
	template_name = 'purchase_list.html'
	context_object_name = 'purchase_list'
	def get_queryset(self):
		super().get_queryset()
		queryset = Purchase.objects.filter(buyer__username=self.request.user)
		return queryset


class PurchaseReturnView(CreateView):
	model = PurchaseReturn
	template_name = 'return.html'
	success_url = '/'
	form_class = PurchaseReturnForm
	def form_valid(self, form):
		object = form.save(commit=False)
		purchase = Purchase.objects.get(id=self.request.POST['purchases_pk'])
		if PurchaseReturn.objects.filter(purchase=purchase):
			raise ValidationError('Товар уже был отправлен на возврат')
		elif purchase.purchase_time + timedelta(minutes=3) < timezone.now():
			raise ValidationError('Чувак не успел, 3 минуты прошло))')
		object.purchase = purchase
		object.save()
		return super().form_valid(form=form)



class PurchaseDeleteView(DeleteView):
	model = Purchase
	success_url = '/'
	template_name = 'purchase_delete.html'
	def post(self, request, *args, **kwargs):
		products_pk = self.request.POST['purchases_pk']
		products_price = self.request.POST['purchases_price']
		products_quantity = self.request.POST['purchases_quantity']
		products_buyer = self.request.POST['purchases_buyer']
		product = Product.objects.get(id=products_pk)
		product.quantity += int(products_quantity)
		product.save()
		user = CustomUser.objects.get(id=products_buyer)
		user.wallet += int(products_quantity) * int(products_price)
		user.save()
		return super().post(request, *args, **kwargs)


class PurchaseReturnDeleteView(DeleteView):
	model = PurchaseReturn
	success_url = '/'
	template_name = 'delete_purchase_return.html'














