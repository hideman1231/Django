from django.test import TestCase, Client
from myshop.models import CustomUser, Product
from django.urls import reverse
from myshop.forms import MyRegisterForm, CreateProductsForm
from django.contrib.auth.forms import AuthenticationForm
import math
import pdb
from PIL import Image


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
        self.failUnless(isinstance(response.context['form'], CreateProductsForm))

    def test_create_product_get_failure(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_create_product_succes(self):
        image = Image.open(r'D:\Desktop\testick\shop\media\c25c94fe96_1000.jpg')
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={'name':'mouse','photo':image,'description':'dblff','price':400,'quantity':33})
        pdb.set_trace()

    def test_create_product_failure(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={'description':'dblff','price':400,'quantity':33})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Product.objects.count(), 0)


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


class UpdateProductViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='abc', password='123')
        self.product = Product.objects.create()
        self.url = reverse('product_update' kwargs={'pk':self.product.pk})

    def test_update_product_get_succes(self):
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(self.url)
        pdb.set_trace()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_update.html')



    def test_update_product_succes(self):
        pass

