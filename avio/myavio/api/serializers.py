from myavio.models import MyUser, Post, LikePost, UserProfile, Comment
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='rest_profile',
        lookup_field='username',
        lookup_url_kwarg='user__username'
    )

    class Meta:
        model = Comment
        fields = ('user', 'text')


class LikePostSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='rest_profile',
        lookup_field='username',
        lookup_url_kwarg='user__username'
    )

    class Meta:
        model = LikePost
        fields = ('user', )


class PostSerializer(serializers.ModelSerializer):
    post_likes = LikePostSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'created_at', 'updated_at', 'text', 'photo',
                  'post_likes', 'comments')


class MyUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'password', 'password2', 'posts')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password mismatch')
        return data

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = MyUserRegisterSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'photo', 'bio')


class CDLikePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikePost
        fields = ('post', )
        read_only = ('user', )


class CUDCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('post', 'text')
        read_only = ('user', )

