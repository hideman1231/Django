from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, Post, LikePost, UserProfile, Comment
from django import forms


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('photo', 'bio')


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('photo', 'text')


class LikePostForm(forms.ModelForm):

    class Meta:
        model = LikePost
        fields = ('post', )
        widgets = {'post': forms.HiddenInput()}


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', )
