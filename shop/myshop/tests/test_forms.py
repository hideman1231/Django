from django.test import TestCase
from myshop.forms import CreatePurchaseForm


class CreatePurchaseFormTest(TestCase):
    def test_quantity(self):
        form_data = {'quantity': 0}
        form = CreatePurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())
