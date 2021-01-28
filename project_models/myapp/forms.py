from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Comment


class SearchCommentsForm(forms.Form):
	content = forms.CharField(max_length=20)
	my_comment = forms.BooleanField(required=False)


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['article','content']


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


class UpdateUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['password']
	password = forms.CharField(
		strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )
	def __init__(self, user, *args, **kwargs):
		self.user = user
		super().__init__(*args, **kwargs)






