from django.urls import path
from .views import product_list, product_detail, add_to_cart, cart_detail, remove_from_cart, decrease_quantity, \
    increase_quantity, checkout, order_history, order_success, complete_order, card_payment, profile, \
    logout_view, register

urlpatterns = [
    path('', product_list, name='product_list'),
    path('register/',register,name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:product_id>/', increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', decrease_quantity, name='decrease_quantity'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_history, name='order_history'),
    path('success/<int:order_id>/',order_success,name='order_success'),
    path('complete_order/',complete_order,name='complete_order'),
    path('card_payment/',card_payment,name='card_payment'),
]




