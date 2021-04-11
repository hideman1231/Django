from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from avio import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profiles.save()


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profiles'
    )
    photo = models.ImageField(
        default=r'D:\Desktop\testick\avio\media\images.png',
        blank=True
    )
    bio = models.TextField()


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    created_at = models.DateField(auto_now=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    text = models.TextField()
    photo = models.ImageField(null=True)

    class Meta:
        ordering = ['-created_at']


class LikePost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_likes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_likes'
    )

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self',
        default=None,
        blank=True, null=True,
        on_delete=models.CASCADE,
    )
