from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import MyRegisterForm, CreateProductsForm, CreatePurchaseForm, PurchaseReturnForm
from .models import CustomUser, Product, Purchase, PurchaseReturn
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def my_handler(sender, **kwargs):
    print('succes register')


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
    extra_context = {'form_create_purchare': CreatePurchaseForm}
    ordering = '-id'
    paginate_by = 3


class CreateProductsView(PermissionRequiredMixin, CreateView):
    permission_required = 'is_superuser'
    model = Product
    form_class = CreateProductsForm
    template_name = 'product_create.html'
    success_url = '/'


class ProductListView(PermissionRequiredMixin, ListView):
    permission_required = 'is_superuser'
    model = Product
    template_name = 'product_list.html'
    ordering = '-id'


class UpdateProductView(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_superuser'
    model = Product
    template_name = 'product_update.html'
    success_url = '/'
    fields = '__all__'


class ProductReturnListView(PermissionRequiredMixin, ListView):
    permission_required = 'is_superuser'
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
        if object.quantity > product.quantity:
            messages.error(self.request, 'Не хватает товара')
            return redirect('/')
        elif self.request.user.wallet < suma:
            messages.error(self.request, 'Не хватает денег')
            return redirect('/')
        else:
            product.quantity = product.quantity - object.quantity
            product.save()
            user = self.request.user
            user.wallet -= suma
            user.save()
        return super().form_valid(form=form)

    def form_invalid(self, form):
        messages.error(self.request, 'Укажите количество')
        return redirect('/')


class PurchaseListView(ListView):
    model = Purchase
    template_name = 'purchase_list.html'
    context_object_name = 'purchase_list'

    def get_queryset(self):
        return super().get_queryset().filter(buyer=self.request.user)

    def get_context_data(self, **kwargs):
        click = self.request.session.get('click', 0)
        click += 1
        self.request.session['click'] = click
        return super().get_context_data(click=click, **kwargs)


class PurchaseReturnView(CreateView):
    model = PurchaseReturn
    template_name = 'return.html'
    success_url = '/mypurchase/'
    form_class = PurchaseReturnForm

    def form_valid(self, form):
        object = form.save(commit=False)
        purchase = Purchase.objects.get(id=self.request.POST['purchases_pk'])
        if PurchaseReturn.objects.filter(purchase=purchase):
            messages.error(self.request, 'Товар уже был отправлен на возврат')
            return redirect('/mypurchase/')
        elif purchase.purchase_time + timedelta(minutes=3) < timezone.now():
            messages.error(self.request, 'Чувак не успел, 3 минуты прошло))')
            return redirect('/mypurchase/')
        object.purchase = purchase
        object.save()
        return super().form_valid(form=form)


class PurchaseDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'is_superuser'
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


class PurchaseReturnDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'is_superuser'
    model = PurchaseReturn
    success_url = '/'
    template_name = 'delete_purchase_return.html'
