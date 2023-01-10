from django.shortcuts import render
from category.models import Category, Subcategory
from order.models import Order, OrderProduct, Payment
from cart.models import Cart, CartItem
from userProfile.models import Account, Address
from product.models import Product


def order_confirmation(request):
    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')


    if request.method == 'POST':

        shipToDiff = request.POST.getlist('checkbox')
        shipToDiff = True if shipToDiff==['on'] else False
        
        selected_address = request.POST.get('flexRadioDefault')
        payment_method = request.POST.get('payment_option')


        if shipToDiff or request.session['email']=='guest@gmail.com':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone_number = request.POST['phone_number']
            email = request.POST['email']
            address = request.POST['address']
            town = request.POST['town']
            state = request.POST['state']
            pincode = request.POST['pincode']
            type = request.POST.get('type')

            user = Account.objects.get(email=request.user)

            addressObj = Address.objects.create(first_name=first_name,last_name=last_name,phone_number=phone_number,email=email,address=address,town=town,state=state,pincode=pincode,type=type,user=user)
            addressObj.save()
    
        else:
            addressObj = Address.objects.get(id=selected_address)
        
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(user=request.user)
        
        cart_total = 0
        cart_discount = 0

        for i in cart_items:
            cart_total += i.product.price * i.quantity

        if cart.coupon_applied:
            cart_discount = (cart_total*cart.coupon.percentage)/100
            cart_total = cart_total - cart_discount

        if payment_method == 'COD':
            status = 'Confirmed'
        elif payment_method == 'RZP':
            status = 'Paid'
        elif payment_method == 'PYP':
            status = 'Paid'

        payment = Payment.objects.create(user=request.user,method=payment_method,amount=cart_total,status=status)
        payment.save()

        order = Order.objects.create(user=request.user,address=addressObj,payment=payment,total=cart_total)
        order.save()

        total = 0

        for i in cart_items:
            subtotal = i.product.price * i.quantity
            order_product = OrderProduct.objects.create(user=request.user,order=order,product=i.product,quantity=i.quantity,have_size=i.have_size,size=i.size,subtotal=subtotal)
            order_product.save()
            total += subtotal
        
        cart.delete()
        cart_items.delete()

        
        order_products = OrderProduct.objects.filter(order=order)

        for i in order_products:
            product = Product.objects.get(id=i.product.id)
            if product.have_size:
                print('. . . . . ',i.size)
                if i.size == 'S':
                    product.sizestockS -= i.quantity
                    product.save()
                elif i.size == 'M':
                    product.sizestockM -= i.quantity
                    product.save()
                else:
                    product.sizestockL -= i.quantity
                    product.save()
            else:
                product.nonsizestock -= i.quantity
                product.save()

        context = {'category':hcategory,'sub_category':hsub_category,'order':order,'order_products':order_products}
        return render(request,'user/order-confirmation.html',context)