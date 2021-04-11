from django.urls import path, include
from avio import settings
from django.conf.urls.static import static
from .views import (HomeView, UserLoginView, UserRegisterView,
                    UserLogoutView, UserProfileDetailView, CreatePostView,
                    LikeDislikeView, MyLikePostList, UpdatePostView,
                    DeletePostView, UpdateProfileView, PostDetailView,
                    PostDetailCommentListView, CreateCommentView)
from .api.resources import (UserRegisterAPIView, UserProfileAPIView, PostViewSet,
                            LikePostAPIView, CommentViewSet)
from rest_framework import routers


router = routers.SimpleRouter()
router.register('user', UserRegisterAPIView)
router.register('post', PostViewSet)
router.register('comment', CommentViewSet)

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('profile/<str:username>/', UserProfileDetailView.as_view(), name='profile'),
    path('profile/<str:username>/change/', UpdateProfileView.as_view(), name='update_profile'),
    path('like-dislike/<int:pk>/', LikeDislikeView.as_view(), name='like_dislike'),
    path('change-post/<int:pk>/', UpdatePostView.as_view(), name='update_post'),
    path('delete-post/<int:pk>/', DeletePostView.as_view(), name='delete_post'),
    path('profile/<str:username>/liked/', MyLikePostList.as_view(), name='my_like_post'),
    path('post/<int:pk>/liked/users/', PostDetailView.as_view(), name='my_like_user'),
    path('post/<int:pk>/comments/', PostDetailCommentListView.as_view(), name='comments'),
    path('post/<int:pk>/create-comment/', CreateCommentView.as_view(), name='create_comment'),

    # REST
    path('api/', include(router.urls)),
    path('api/profile/<str:user__username>/', UserProfileAPIView.as_view(), name='rest_profile'),
    path('api/like-dislike/', LikePostAPIView.as_view(), name='rest_like_dislike'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
