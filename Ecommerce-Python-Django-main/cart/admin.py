from django.contrib import admin
from . models import CartItem, Coupon, Cart

# Register your models here.
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Coupon)
