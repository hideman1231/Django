from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, UserProfile, Post, LikePost, Comment

admin.site.register(MyUser, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Comment)
