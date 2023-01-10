from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>', views.remove_from_cart, name='remove_from_cart'),
    path('add_quantity_cart_item/<int:id>', views.add_quantity_cart_item, name='add_quantity_cart_item'),
    path('subtract_quantity_cart_item/<int:id>', views.subtract_quantity_cart_item, name='subtract_quantity_cart_item'),
    path('clear_cart', views.clear_cart, name='clear_cart'),
    path('cart_view', views.cart_view, name='cart_view'),

    path('user_checkout', views.user_checkout, name='user_checkout'),

    path('add_coupon/<str:code>', views.add_coupon, name='add_coupon'),
    path('remove_coupon/<int:id>', views.remove_coupon, name='remove_coupon')
]