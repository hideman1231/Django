from django.urls import reverse
from rest_framework.test import APITestCase
from myshop.api.serializers import CustomUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from myshop.models import CustomUser, Product, Purchase, PurchaseReturn
from http import HTTPStatus
from rest_framework import status


class CustomUserViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = CustomUser.objects.create(username='A1', password='12')
        self.user2 = CustomUser.objects.create(username='A2', password='13')
        self.user3 = CustomUser.objects.create(username='A3', password='3')
        self.user4 = CustomUser.objects.create(username='A4', password='1')

    def test_user_no_login(self):
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_user_list(self):
        url = reverse('users-list')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), CustomUser.objects.count())

    def test_user_retrieve(self):
        url = reverse('users-detail', kwargs={'pk': self.user3.pk})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_create_succes(self):
        url = reverse('users-list')
        self.client.force_authenticate(user=self.user1)
        data = {'username':'aa', 'password':'164', 'wallet':'1000'}
        response = self.client.post(url, data)
        username = CustomUser.objects.all().last().username
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], username)

    def test_user_create_failure(self):
        url = reverse('users-list')
        self.client.force_authenticate(user=self.user1)
        data = {'username':'aa','wallet':'1000'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_user_patch(self):
        url = reverse('users-detail', kwargs={'pk': self.user4.pk})
        self.client.force_authenticate(user=self.user1)
        data = {'username':'nea4'}
        response = self.client.patch(url, data)
        username = CustomUser.objects.get(id=self.user4.pk).username
        self.assertEqual(response.data['username'], username)
        self.assertEqual(response.status_code, 200)

    def test_user_put(self):
        url = reverse('users-detail', kwargs={'pk': self.user4.pk})
        self.client.force_authenticate(user=self.user1)
        data = {'username':'nea4', 'password':'123', 'wallet':2000}
        response = self.client.put(url, data)
        username = CustomUser.objects.get(id=self.user4.pk).username
        password = CustomUser.objects.get(id=self.user4.pk).password
        wallet = CustomUser.objects.get(id=self.user4.pk).wallet
        self.assertEqual(response.data['username'], username)
        self.assertEqual(response.data['password'], password)
        self.assertEqual(response.data['wallet'], wallet)
        self.assertEqual(response.status_code, 200)

    def test_user_destroy(self):
        url = reverse('users-detail', args=[self.user2.pk])
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(url)

class PurchaseViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username='test', password='12')
        self.product1 = Product.objects.create(name='aa', description='ff', price=100, quantity=200)
        self.product2 = Product.objects.create(name='bb0', description='weweff', price=10, quantity=300) 
        self.purchase1 = Purchase.objects.create(buyer=self.user, product=self.product1, quantity=2)
        self.purchase2 = Purchase.objects.create(buyer=self.user, product=self.product2, quantity=5)

    def test_purchase_no_login(self):
        url = reverse('purchases-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_purchase_list(self):
        url = reverse('purchases-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), Purchase.objects.count())

    def test_purchase_retrieve(self):
        url = reverse('purchases-detail', kwargs={'pk':self.purchase1.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_purchase_create_succes(self):
        url = reverse('purchases-list')
        self.client.force_authenticate(user=self.user)
        data = {'product':self.product2.pk, 'quantity':7}
        response = self.client.post(url, data)
        product_quantity = Product.objects.get(id=response.data['product']).quantity
        purchase_quantity = response.data['quantity']
        suma = purchase_quantity * Product.objects.get(id=response.data['product']).price
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user.wallet, 1000 - suma)
        self.assertEqual(product_quantity, 300 - purchase_quantity)

    def test_purchase_create_failure_not_enough_product(self):
        url = reverse('purchases-list')
        self.client.force_authenticate(user=self.user)
        data = {'product':self.product2.pk, 'quantity':700}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Товара не хватает', response.data['non_field_errors'])

    def test_purchase_create_failure_not_enough_money(self):
        url = reverse('purchases-list')
        self.client.force_authenticate(user=self.user)
        data = {'product':self.product1.pk, 'quantity':100}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('У вас не хватает зелени', response.data['non_field_errors'])

   
class PurchaseReturnViewSet(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = CustomUser.objects.create(username='eieie', password='fd12')
        self.user2 = CustomUser.objects.create(username='terreerest', password='1df2')
        self.product1 = Product.objects.create(name='aa', description='ff', price=20, quantity=200)
        self.product2 = Product.objects.create(name='bb0', description='weweff', price=10, quantity=300) 
        self.purchase1 = Purchase.objects.create(buyer=self.user1, product=self.product1, quantity=2)
        self.purchase2 = Purchase.objects.create(buyer=self.user2, product=self.product2, quantity=4)
        self.purchase3 = Purchase.objects.create(buyer=self.user1, product=self.product2, quantity=5)
        self.purchase_return1 = PurchaseReturn.objects.create(purchase=self.purchase1)
        self.purchase_return2 = PurchaseReturn.objects.create(purchase=self.purchase2)

    def test_purchase_no_login(self):
        url = reverse('purchase_returns-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_purchase_return_list(self):
        url = reverse('purchase_returns-list')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), PurchaseReturn.objects.count())

    def test_purchase_return_retrieve(self):
        url = reverse('purchase_returns-detail', args=[self.purchase_return1.pk])
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_purchase_return_create(self):
        url = reverse('purchase_returns-list')
        self.client.force_authenticate(user=self.user1)
        data = {'purchase':self.purchase3.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_purchase_return_create_another_user(self):
        url = reverse('purchase_returns-list')
        self.client.force_authenticate(user=self.user1)
        data = {'purchase':self.purchase2.pk}
        response = self.client.post(url, data)
        self.assertIn('Это не твоя покупка!', response.data['purchase'])
        self.assertEqual(response.status_code, 400)

    def test_purchase_return_create_resending(self):
        url = reverse('purchase_returns-list')
        self.client.force_authenticate(user=self.user1)
        data = {'purchase':self.purchase3.pk}
        self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Чувак ты уже отправлял это товар на возврат', response.data['purchase'])
