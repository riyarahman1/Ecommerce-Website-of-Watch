from django.db import models
from userProfile.models import Account
from product.models import Product

class Coupon(models.Model):
    code = models.CharField(max_length=50,unique=True)
    percentage = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.code

class Cart(models.Model):
    user        =   models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    coupon      =  models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True)
    coupon_applied =  models.BooleanField(default=False)
    total = models.FloatField(null = True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    user        =   models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    product     =   models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity    =   models.IntegerField(null=True)
    subtotal = models.FloatField(null = True)
    have_size = models.BooleanField(default=False)
    size = models.CharField(max_length=1, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name

