from django import forms
from .models import CustomUser, Product, Purchase, PurchaseReturn


class MyRegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'wallet']
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = False


class CreatePurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['quantity']

    def clean_quantity(self):
        data = self.cleaned_data.get('quantity')
        if data == 0:
            raise forms.ValidationError('Выберите количество')
        return data


class PurchaseReturnForm(forms.ModelForm):
    class Meta:
        model = PurchaseReturn
        exclude = ['purchase']
