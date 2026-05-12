from django.urls import path
from .views import product_list, product_detail, add_to_cart, cart_detail, remove_from_cart, decrease_quantity, \
    increase_quantity, checkout, order_history

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:product_id>/', increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', decrease_quantity, name='decrease_quantity'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_history, name='order_history'),
]