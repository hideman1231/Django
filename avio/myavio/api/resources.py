from rest_framework.response import Response
from rest_framework import viewsets, status, permissions, generics, pagination
from rest_framework.decorators import action
from myavio.api.serializers import (MyUserRegisterSerializer, UserProfileSerializer,
                                    PostSerializer, CDLikePostSerializer, CUDCommentSerializer)
from myavio.models import MyUser, Post, LikePost, UserProfile, Comment
from myavio.api.permissions import IsOwner
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.settings import api_settings
from rest_framework.exceptions import ValidationError


class UserRegisterAPIView(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserRegisterSerializer
    http_method_names = ['post']


class UserProfileAPIView(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user__username'
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            self.permission_classes += [IsOwner]
        return super().get_permissions()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['post', 'patch', 'delete']
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            self.permission_classes += [IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class LikePostAPIView(generics.GenericAPIView):
    queryset = LikePost.objects.all()
    serializer_class = CDLikePostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def perform_destroy(self, instance):
        instance.delete()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, like_post, *args, **kwargs):
        instance = like_post
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        post_pk = request.data['post']
        try:
            post = Post.objects.get(id=post_pk)
        except ObjectDoesNotExist:
            raise ValidationError('The post does not exist')
        user = request.user
        try:
            like_post = LikePost.objects.get(post=post, user=user)
        except ObjectDoesNotExist:
            return self.create(request, *args, **kwargs)
        else:
            return self.destroy(request, like_post, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CUDCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post', 'patch', 'delete']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            self.permission_classes += [IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)



