from .models import CustomUser, Product, Purchase, PurchaseReturn
from django import forms


class MyRegisterForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ['username','password','wallet']
	password = forms.CharField(
		strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )
	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user


class CreateProductsForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = '__all__'


class CreatePurchaseForm(forms.ModelForm):
	class Meta:
		model = Purchase
		fields = ['quantity']


class PurchaseReturnForm(forms.ModelForm):
	class Meta:
		model = PurchaseReturn
		exclude = ['purchase']










