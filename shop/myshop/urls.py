from django.urls import path, include
from .views import (ProductsView, LoginUserView, LogoutUserView,
                    RegisterUserView, CreateProductsView, ProductListView,
                    UpdateProductView, ProductReturnListView, PurchasesView,
                    PurchaseListView, PurchaseReturnView, PurchaseDeleteView,
                    PurchaseReturnDeleteView)
from myshop.api.resources import (AuthorViewSet, BookViewSet, ExampleView,
                                  CustomUserViewSet, PurchaseViewSet,
                                  PurchaseReturnViewSet)
from rest_framework import routers
from rest_framework.authtoken import views


router = routers.SimpleRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'purchases', PurchaseViewSet, basename='purchases')
router.register(r'purchase_returns', PurchaseReturnViewSet, basename='purchase_returns')


urlpatterns = [
    path('', ProductsView.as_view(), name='index'),
    path('api/', include(router.urls)),
    path('api/auth/', ExampleView.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('product_create/', CreateProductsView.as_view(), name='product_create'),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/update/',
         UpdateProductView.as_view(), name='product_update'),
    path('product_return/', ProductReturnListView.as_view(),
         name='product_return'),
    path('purchase_create/', PurchasesView.as_view(), name='purchase_create'),
    path('mypurchase/', PurchaseListView.as_view(), name='mypurchase'),
    path('return/', PurchaseReturnView.as_view(), name='return'),
    path('delete_purchase/<int:pk>/',
         PurchaseDeleteView.as_view(), name='delete_purchase'),
    path('delete_purchase_return/<int:pk>/',
         PurchaseReturnDeleteView.as_view(), name='delete_purchase_return')

]
