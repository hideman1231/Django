from django.test import TestCase

from myshop.models import Product


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name='boll',
            description='good basketball ball',
            price=300,
            quantity=100
        )

    def test_name_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)


    def test_photo_null(self):
        product = Product.objects.get(id=1)
        null = product._meta.get_field('photo').null

