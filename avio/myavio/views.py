from django.views.generic import TemplateView, DetailView
from myavio.models import UserProfile, MyUser, Post, LikePost, Comment
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import (CreateView, ListView, DetailView,
                                  UpdateView, DeleteView, TemplateView,
                                  View)
from django.urls import reverse_lazy, reverse
from myavio.forms import (MyUserCreationForm, PostForm, LikePostForm,
                          ProfileForm, CommentForm)
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
import requests
from bs4 import BeautifulSoup
import re


def parser_weather():
    url = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D1%85%D0%B0%D1%80%D1%8C%D0%BA%D0%BE%D0%B2'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    today_weather = soup.find_all('p', class_='today-temp')
    return today_weather[0]


class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        today_weather = parser_weather()
        context = self.get_context_data(**kwargs)
        degree = re.search(r'[-+]?\d+', today_weather.text)
        if int(degree.group()) <= -10:
            prompt = 'Dress warmly!!!'
        elif -10 > int(degree.group()) > 10:
            prompt = 'What a heat)'
        else:
            prompt = 'Nice weather)'
        context['weather'] = f'{today_weather.text}. {prompt}'
        return self.render_to_response(context)


class UserProfileDetailView(DetailView):
    model = MyUser
    template_name = 'profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    paginate_by = 3


class UpdateProfileView(UpdateView):
    model = UserProfile
    template_name = 'update_profile.html'
    slug_url_kwarg = 'user__username'
    slug_field = 'user__username'
    form_class = ProfileForm

    def get_success_url(self):
        user = self.request.user
        return reverse('profile', kwargs={'username': user.username})


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        return reverse('profile', kwargs={'username': user.username})


class UserRegisterView(CreateView):
    model = MyUser
    form_class = MyUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('index')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        return super().form_valid(form=form)

    def get_success_url(self):
        user = self.request.user
        return reverse('profile', kwargs={'username': user.username})


class LikeDislikeView(View):

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = Post.objects.get(id=pk)
        user = self.request.user
        like, status = LikePost.objects.get_or_create(user=user, post=post)
        if not status:
            like.delete()
        if self.request.META['HTTP_REFERER'] == fr'http://127.0.0.1:8000/profile/{user}/liked/':
            return redirect(reverse('my_like_post', kwargs={'username': post.user.username}))
        return redirect(reverse('profile', kwargs={'username': post.user.username}))


class MyLikePostList(ListView):
    model = Post
    template_name = 'my_like_post.html'
    context_object_name = 'my_like_list'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(post_likes__user=user)


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    form_class = PostForm

    def get_success_url(self):
        user = self.request.user
        return reverse('profile', kwargs={'username': user.username})


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'

    def get_success_url(self):
        user = self.request.user
        return reverse('profile', kwargs={'username': user.username})


class PostDetailView(DetailView):
    model = Post
    template_name = 'my_user_likes.html'
    context_object_name = 'post'


class CreateCommentView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        pk = self.kwargs['pk']
        post = Post.objects.get(id=pk)
        object.post = post
        if 'comment_pk' in self.request.POST:
            comment_pk = self.request.POST.get('comment_pk')
            comment = Comment.objects.get(id=comment_pk)
            object.parent = comment
        return super().form_valid(form=form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('comments', kwargs={'pk': pk})


class PostDetailCommentListView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'create_comment.html'
    extra_context = {'comment_form': CommentForm}
