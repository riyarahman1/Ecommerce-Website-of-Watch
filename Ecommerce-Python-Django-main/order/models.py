from django.db import models
from userProfile.models import Account, Address
from product.models import Product

# Create your models here.
class Payment(models.Model):

    user =  models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    method = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.method

class Order(models.Model):

    STATUS = (
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned')
    )
    
    user        =   models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    address     =   models.ForeignKey(Address,on_delete=models.CASCADE, null=True)
    date        =   models.DateField(null=True,auto_now_add=True)
    payment     =   models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True)
    total       =   models.FloatField(max_length=200,null=True)
    status      =   models.CharField(max_length=30, choices=STATUS, default='Confirmed')
    reason      =   models.CharField(max_length=200, default='Reason')
    def __str__(self):
        return self.user.first_name

class OrderProduct(models.Model):
    user        =   models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    order       =   models.ForeignKey(Order,on_delete=models.CASCADE, null=True)
    product     =   models.ForeignKey(Product,on_delete=models.CASCADE, null=True)
    quantity    =   models.IntegerField(null=True)
    subtotal    =   models.FloatField(max_length=200,null=True)
    have_size   =   models.BooleanField(default=False)
    size        =   models.CharField(max_length=1, blank=True)
    
    def sub_total(self):
        return self.subtotal * self.quantity

    def __str__(self):
        return str(self.product)