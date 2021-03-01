from django.test import TestCase, Client
from myshop.models import CustomUser, Product, Purchase, PurchaseReturn
from django.urls import reverse
from myshop.forms import MyRegisterForm, CreateProductsForm, CreatePurchaseForm, PurchaseReturnForm
from django.contrib.auth.forms import AuthenticationForm
import math
import pdb
from datetime import timedelta
from django.utils import timezone


class LoginUserViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='testuser', password='123')
        self.user.set_password(self.user.password)
        self.user.save()
        self.url = reverse('login')

    def test_user_login_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.failUnless(isinstance(
            response.context['form'], AuthenticationForm))

    def test_user_login_succes(self):
        response = self.client.post(
            self.url, {'username': 'testuser', 'password': '123'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_user_login_failure(self):
        response = self.client.post(
            self.url, {'username': 'fddfdf', 'password': 'dfdfdfdf'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

    def test_user_login_redirect(self):
        response = self.client.post(
            self.url, {'username': 'testuser', 'password': '123'})
        self.assertEqual(response.status_code, 302)


class LogoutUserViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='testuser', password='123')

    def test_user_logout(self):
        self.client.force_login(self.user)
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.url, '/')


class RegisterUserView(TestCase):

    def setUp(self):
        self.url = reverse('register')

    def test_user_register_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.failUnless(isinstance(response.context['form'], MyRegisterForm))

    def test_user_register_succes(self):
        response = self.client.post(
            self.url, data={'username': 'testuser', 'password': '123', 'wallet': 1000})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(response.url, '/')

    def test_user_register_failure(self):
        response = self.client.post(
            self.url, data={'password': '123', 'wallet': 1000})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(CustomUser.objects.count(), 0)


class ProductsViewTest(TestCase):

    def setUp(self):
        self.url = reverse('index')
        for i in range(10):
            Product.objects.create(
                name=f'name{i}',
                description=f'description{i}',
                price=i + 1000,
                quantity=i + 200,
            )

    def test_products_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_products_view_get_paginations(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.context['object_list'].count(),
            response.context['paginator'].per_page)
        self.assertEqual(response.context['paginator'].num_pages,
                         math.ceil(response.context['paginator'].object_list.count() / response.context['paginator'].per_page))


class CreateProductsViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='abc', password='123')
        self.url = reverse('product_create')

    def test_create_product_get_succes(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_create.html')
        self.failUnless(isinstance(
            response.context['form'], CreateProductsForm))

    def test_create_product_get_failure(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_create_product_succes(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={
                                    'name': 'mouse', 'description': 'dblff', 'price': 400, 'quantity': 33})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(response.url, '/')

    def test_create_product_failure(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, data={'description': 'dblff', 'price': 400, 'quantity': 33})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Product.objects.count(), 0)

    def test_update_product_no_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class ProductListViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='abc', password='123')
        self.url = reverse('product_list')

    def test_product_list_get_succes(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_list.html')

    def test_product_list_get_failure(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_product_list_no_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class UpdateProductViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='abc', password='123')
        self.product = Product.objects.create(
            name='aa', description='ff', price=200, quantity=200)
        self.url = reverse('product_update', kwargs={'pk': self.product.pk})

    def test_update_product_get_succes(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_update.html')

    def test_update_product_get_failure(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_product_post_succes(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={
                                    'name': 'aaa', 'description': 'bb', 'price': 100, 'quantity': 100})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        self.assertNotEqual(Product.objects.get(id=1).name, self.product.name)

    def test_update_product_post_failure(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, data={'description': 'bbb', 'price': 100, 'quantity': 100})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Product.objects.get(id=1).name, self.product.name)

    def test_update_product_no_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class ProductReturnListViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='abc', password='123')
        self.url = reverse('product_return')

    def product_return_get_succes(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_return.html')

    def product_return_get_failure(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def product_return_no_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class PurchasesViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='abc', password='123')
        self.url = reverse('purchase_create')
        self.product = Product.objects.create(
            name='aa', description='ff', price=50, quantity=200)

    def test_purchase_create_get_succes(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'purchase_create.html')
        self.failUnless(isinstance(
            response.context['form'], CreatePurchaseForm))

    def test_purchase_create_post_succes(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, data={'product_pk': self.product.pk, 'quantity': 5}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Purchase.objects.count(), 1)

    def test_purchase_create_post_succes_redirect(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, data={'product_pk': self.product.pk, 'quantity': 5})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_purchase_create_post_failure(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, data={'product_pk': self.product.pk})
        self.assertEqual(Purchase.objects.count(), 0)

    def test_purchase_create_post_succes_logic(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, data={'product_pk': self.product.pk, 'quantity': 5}, follow=True)
        self.assertEqual(Product.objects.get(
            id=1).quantity, self.product.quantity - Purchase.objects.get(id=1).quantity)
        self.assertEqual(CustomUser.objects.get(id=1).wallet, self.user.wallet -
                         Purchase.objects.get(id=1).quantity * self.product.price)

    def test_purchase_create_post_failure_logic(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, data={'product_pk': self.product.pk, 'quantity': 500}, follow=True)
        self.assertTrue(response.context['messages'].used)
        self.assertEqual(Purchase.objects.count(), 0)

    def test_purchase_create_no_login(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

class PurchaseListViewTest(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create(username='abc', password='123')
        self.user2 = CustomUser.objects.create(username='mo', password='mo')
        self.url = reverse('mypurchase')
        self.product = Product.objects.create(
            name='aa', description='ff', price=50, quantity=200)
        for i in range(2):
            Purchase.objects.create(
                buyer=self.user1, product=self.product, quantity=i)
        for i in range(3):
            Purchase.objects.create(
                buyer=self.user2, product=self.product, quantity=i)

    def test_purchase_list_get_user1(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.context['purchase_list'].count(
        ), Purchase.objects.filter(buyer=self.user1).count())

    def test_purchase_list_get_user2(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.context['purchase_list'].count(
        ), Purchase.objects.filter(buyer=self.user2).count())

    def test_purchase_list_get_no_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

class PurchaseReturnViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='abc', password='123')
        self.url = reverse('return')
        self.product = Product.objects.create(
            name='aa', description='ff', price=50, quantity=200)
        self.purchase = Purchase.objects.create(
            buyer=self.user, product=self.product, quantity=10)

    def test_purchase_return_create_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'return.html')
        self.failUnless(isinstance(
            response.context['form'], PurchaseReturnForm))

    def test_purchase_return_create_post_succes(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, data={'purchases_pk': self.purchase.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PurchaseReturn.objects.count(), 1)

    def test_purchase_return_create_post_succes_redirect(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, data={'purchases_pk': self.purchase.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/mypurchase/')

    def test_purchase_return_create_post_failure_logic_double_dispatch(self):
        self.client.force_login(self.user)
        self.client.post(
            self.url, data={'purchases_pk': self.purchase.pk}, follow=True)
        response = self.client.post(
            self.url, data={'purchases_pk': self.purchase.pk}, follow=True)
        self.assertTrue(response.context['messages'].used)
        self.assertEqual(PurchaseReturn.objects.count(), 1)

    def test_purchase_return_create_post_failure_logic_correct_user(self):
        user1 = CustomUser.objects.create(
            username='dffdffdqd', password='dffdfd')
        self.client.force_login(user1)
        response = self.client.post(
            self.url, data={'purchases_pk': self.purchase.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/mypurchase/')
        self.assertEqual(PurchaseReturn.objects.count(), 0)

    # def test_purchase_return_create_post_failure_logic_correct_time(self):
    #     self.client.force_login(self.user)
    #     print(self.purchase.purchase_time + timedelta(days=-1))
    #     self.purchase.save()
    #     response = self.client.post(self.url, data={'purchases_pk':self.purchase.pk})
    #     pdb.set_trace()
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, '/mypurchase/')
    #     self.assertEqual(PurchaseReturn.objects.count(), 0)

    def test_purchase_return_create_no_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

class PurchaseDeleteViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='abc', password='123')
        self.user_admin = CustomUser.objects.create(
            username='admin', password='1234')
        self.product = Product.objects.create(
            name='aa', description='ff', price=50, quantity=200)
        self.purchase = Purchase.objects.create(
            buyer=self.user, product=self.product, quantity=10)
        self.url = reverse('delete_purchase', kwargs={'pk': self.purchase.pk})

    def test_purchase_delete_succes(self):
        self.user_admin.is_superuser = True
        self.user_admin.save()
        self.client.force_login(self.user_admin)
        response = self.client.post(self.url, data={'purchases_pk': self.product.pk, 'purchases_price': self.product.price,
                                                    'purchases_quantity': self.purchase.quantity, 'purchases_buyer': self.purchase.buyer.pk})
        self.assertEqual(Product.objects.get(id=1).quantity,
                         self.product.quantity + self.purchase.quantity)
        self.assertEqual(CustomUser.objects.get(
            id=1).wallet, (self.product.price * self.purchase.quantity) + self.user.wallet)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        self.assertEqual(Purchase.objects.count(), 0)

    def test_purchase_delete_failure(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={'purchases_pk': self.product.pk, 'purchases_price': self.product.price,
                                                    'purchases_quantity': self.purchase.quantity, 'purchases_buyer': self.purchase.buyer.pk})
        self.assertEqual(response.status_code, 403)

    def test_purchase_delete_no_login(self):
        response = self.client.post(self.url, data={'purchases_pk': self.product.pk, 'purchases_price': self.product.price,
                                                    'purchases_quantity': self.purchase.quantity, 'purchases_buyer': self.purchase.buyer.pk})
        self.assertEqual(response.status_code, 302)


class PurchaseReturnDeleteView(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='abc', password='123')
        self.user_admin = CustomUser.objects.create(
            username='admin', password='1234')
        self.product = Product.objects.create(
            name='aa', description='ff', price=50, quantity=200)
        self.purchase = Purchase.objects.create(
            buyer=self.user, product=self.product, quantity=10)
        self.purchases_return = PurchaseReturn.objects.create(
            purchase=self.purchase)
        self.url = reverse('delete_purchase_return', kwargs={
                           'pk': self.purchases_return.pk})

    def test_purchase_return_delete_succes(self):
        self.user_admin.is_superuser = True
        self.user_admin.save()
        self.client.force_login(self.user_admin)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        self.assertEqual(PurchaseReturn.objects.count(), 0)

    def test_purchase_return_delete_failure(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_purchase_return_delete_no_login(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
