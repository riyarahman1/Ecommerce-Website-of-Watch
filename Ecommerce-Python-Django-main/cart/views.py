from django.shortcuts import render, redirect
from django.contrib import messages
from category.models import Category, Subcategory
from product.models import Product
from . models import Cart, CartItem, Coupon
from userProfile.models import Address
import razorpay
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from userProfile.views import user_login


def add_to_cart(request,id):
    if 'email' in request.session:

        if request.method == 'POST':
            product = Product.objects.get(id=id)

            quantity = int(request.POST.get('quantity'))

            if product.have_size:
                size = request.POST['size']
            
            subtotal = product.discount_price * quantity

            if Cart.objects.filter(user=request.user).exists():
                cart = Cart.objects.get(user=request.user)
            else:
                cart = Cart.objects.create(user=request.user)

            
            if product.have_size:
                if CartItem.objects.filter(product=product,size=size,user=request.user).exists():
                    cart_item = CartItem.objects.get(product=product,size=size,user=request.user)
                    cart_item.quantity += quantity
                    cart_item.subtotal = product.discount_price * cart_item.quantity
                    cart_item.save()
                else:
                    cart_item = CartItem.objects.create(cart=cart,user=request.user,product=product,quantity=quantity,subtotal=subtotal,have_size=product.have_size,size=size)
                    cart_item.save()
            else:
                if CartItem.objects.filter(product=product,user=request.user).exists():
                    cart_item = CartItem.objects.get(product=product,user=request.user)
                    cart_item.quantity += quantity
                    cart_item.subtotal = product.discount_price * cart_item.quantity
                    cart_item.save()
                else:
                    cart_item = CartItem.objects.create(cart=cart,user=request.user,product=product,quantity=quantity,subtotal=subtotal,have_size=product.have_size)
                    cart_item.save()

            messages.info(request, 'Item added to Cart')

        
            return HttpResponseRedirect(reverse('product_view', kwargs={'id': id}))
            
    else:
        
           return render(request, 'user/user-login.html')

    return redirect(cart_view)

def add_quantity_cart_item(request,id):
    cart_item = CartItem.objects.get(id=id)
    if cart_item.quantity != 10:
        cart_item.quantity += 1
    cart_item.subtotal = cart_item.product.discount_price * cart_item.quantity
    cart_item.save()
    return redirect('cart_view')

def subtract_quantity_cart_item(request,id):
    cart_item = CartItem.objects.get(id=id)
    if cart_item.quantity == 1:
        cart_item.delete()
        if not CartItem.objects.filter(user=request.user).exists():
            cart = Cart.objects.get(user=request.user)
            cart.delete()
    else:
        cart_item.quantity -= 1
    cart_item.subtotal = cart_item.product.discount_price * cart_item.quantity
    cart_item.save()
    return redirect('cart_view')

def remove_from_cart(request,id):
    
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    if not CartItem.objects.filter(user=request.user).exists():
            cart = Cart.objects.get(user=request.user)
            cart.delete()
    messages.success(request,"Cart Item Removed Successfully")
    
    return redirect('cart_view')

def clear_cart(request):

    cart_items = CartItem.objects.filter(user=request.user)
    if cart_items:
        cart_items.delete()
        cart = Cart.objects.filter(user=request.user)
        cart.delete()
        messages.success(request,"Cart Cleared Removed Successfully")
    else:
        messages.success(request,"No Items In Cart")

    return redirect('cart_view')

def cart_view(request):
    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')

    try:
        cart = Cart.objects.get(user=request.user)

        cart_items = CartItem.objects.filter(user=request.user).order_by('product__name')


        cart_total = 0
        cart_discount = 0
        cart_total_discount = 0

        for i in cart_items:
            cart_total += i.product.discount_price * i.quantity

        if cart.coupon_applied:
            cart_discount = (cart_total*cart.coupon.percentage)/100
            cart_total_discount = cart_total - cart_discount

        context = {'category':hcategory,'sub_category':hsub_category,'cart':cart,'cart_items':cart_items,'cart_total':cart_total,'cart_discount':cart_discount,'cart_total_discount':cart_total_discount}
        return render(request,'user/user-cart.html',context)
    except:
        print("No Items in Cart")
        cart_total = 0
        context = {'category':hcategory,'sub_category':hsub_category,'cart_total':cart_total}
        return render(request,'user/user-cart.html',context)


def user_checkout(request):


    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(user=request.user).order_by('-date_added')

    addresses = Address.objects.filter(user=request.user)

    cart_total = 0
    cart_discount = 0
    cart_total_discount = 0

    for i in cart_items:
        cart_total += i.product.discount_price * i.quantity
    if cart.coupon_applied:
        cart_discount = (cart_total*cart.coupon.percentage)/100
        cart_total_discount = cart_total - cart_discount

        client = razorpay.Client(auth = (settings.RAZOR_PAY_KEY_ID, settings.RAZOR_PAY_KEY_SECRET))
        payment = client.order.create({'amount':cart_total_discount * 100, 'currency':'INR', 'payment_capture':1})
    else:
        client = razorpay.Client(auth = (settings.RAZOR_PAY_KEY_ID, settings.RAZOR_PAY_KEY_SECRET))
        payment = client.order.create({'amount':cart_total * 100, 'currency':'INR', 'payment_capture':1})
    

    context = {'category':hcategory,'sub_category':hsub_category,'cart':cart,'cart_items':cart_items,'cart_total':cart_total,'cart_discount':cart_discount,'cart_total_discount':cart_total_discount,'addresses':addresses,'payment':payment}
    return render(request,'user/user-checkout.html',context)


def add_coupon(request,code):
    code = code.upper()
    if Coupon.objects.filter(code=code).exists():
        coupon = Coupon.objects.get(code=code)
        cart = Cart.objects.get(user=request.user)
        cart.coupon = coupon
        cart.coupon_applied = True
        cart.save()
    else:
        messages.success(request,"Invalid Coupon Code")

    return redirect('cart_view')

def remove_coupon(request,id):
    cart = Cart.objects.get(id=id)
    cart.coupon = None
    cart.coupon_applied = False
    cart.save()

    return redirect('cart_view')
