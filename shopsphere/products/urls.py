from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.allproducts_view, name='allproducts'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('order/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_history, name='order_history'),
]