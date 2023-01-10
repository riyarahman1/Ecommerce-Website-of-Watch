from django.shortcuts import render
from product.models import Product
from category.models import Category, Subcategory
from django.core.paginator import Paginator
from django.http import JsonResponse



def product_list(request,category,sub_category,sortby,min,max):

    if request.method == 'POST':
        min = request.POST['min']
        max = request.POST['max']

    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')

    if sortby == 'relevance':
        sortby = 'name'
    elif sortby == 'newest':
        sortby = '-created_date'
    elif sortby == 'lowtohigh':
        sortby = 'price'
    elif sortby == 'hightolow':
        sortby = '-price'

    
    # if category=='MEN':
    #     id=4
    # else:
    #     id=2
    if sub_category == 'None':
        products = Product.objects.filter(category__name=category).order_by(sortby)

        paginator = Paginator(products,6)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        context = {'title':category,'products':products,'category':hcategory,'sub_category':hsub_category,'currentCat':category,'currentSubcat':sub_category,'min':min,'max':max}
    else:
        products = Product.objects.filter(sub_category__name=sub_category).order_by(sortby)

        paginator = Paginator(products,6)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        context = {'title':sub_category,'products':products,'category':hcategory,'sub_category':hsub_category,'currentCat':category,'currentSubcat':sub_category,'min':min,'max':max}
    
    return render(request,'user/shop-product-filter.html', context)

def product_view(request,id):
    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')

    product = Product.objects.get(id=id)

    context = {'category':hcategory,'sub_category':hsub_category,'product':product}

    return render(request, 'user/shop-product-view.html',context)


def get_size_info(request):
    if request.method == "POST":
        size = request.POST['size']
        id = request.POST['id']

        product = Product.objects.get(id=id)

        if size == 'S':
            sizeStock = product.sizestockS
        elif size == 'M':
            sizeStock = product.sizestockM
        elif size == 'L':
            sizeStock = product.sizestockL

        return JsonResponse({'sizeStock':sizeStock,'size':size})
    return JsonResponse({})


