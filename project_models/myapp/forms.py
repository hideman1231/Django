from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Comment


class ContentCommentsForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']


class MyLoginForm(AuthenticationForm, forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','password']
	def get_form_kwargs(self):
		return self.model


class MyRegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','password']
	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user





