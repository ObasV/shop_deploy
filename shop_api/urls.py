from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.landing, name = 'landing'),
  path('products', views.ProductList.as_view()),
  path('products/<int:pk>', views.ProductDetail.as_view()),
  path('products/create', views.ProductCreate.as_view()),
  path('products/<int:pk>/update', views.ProductUpdate.as_view()),
  path('products/<int:pk>/delete', views.ProductDelete.as_view()),
  # Add URL patterns for Order and Cancel Order views here
  path('orders', views.OrderList.as_view()),
  path('orders/<int:pk>', views.OrderDetail.as_view()),
  path('orders/<int:pk>/delete', views.OrderDelete.as_view()),
  path('orders/create', views.OrderCreate.as_view())
]
