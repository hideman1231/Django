from django.urls import path
from .views import ProductsView, LoginUserView, LogoutUserView, RegisterUserView, CreateProductsView, ProductListView, UpdateProductView, ProductReturnListView, PurchasesView, PurchaseListView, PurchaseReturnView, PurchaseDeleteView, PurchaseReturnDeleteView

urlpatterns = [
	path('', ProductsView.as_view(), name='index'),
	path('login/', LoginUserView.as_view(), name='login'),
	path('logout/', LogoutUserView.as_view(), name='logout'),
	path('register/', RegisterUserView.as_view(), name='register'),
	path('product_create/', CreateProductsView.as_view(), name='product_create'),
	path('product/', ProductListView.as_view(), name='product_list'),
	path('product/<int:pk>/update/', UpdateProductView.as_view(), name='product_update'),
	path('product_return/', ProductReturnListView.as_view(), name='product_return'),
	path('purchase_create/<int:pk>/', PurchasesView.as_view(), name='purchase_create'),
	path('mypurchase/', PurchaseListView.as_view(), name='mypurchase'),
	path('return/', PurchaseReturnView.as_view(), name='return'),
	path('delete_purchase/<int:pk>/', PurchaseDeleteView.as_view(), name='delete_purchase'),
	path('delete_purchase_return/<int:pk>/', PurchaseReturnDeleteView.as_view(), name='delete_purchase_return')

]