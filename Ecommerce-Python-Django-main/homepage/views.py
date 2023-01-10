from django.shortcuts import render
from product.models import Product
from category.models import Category,Subcategory
from django.http import JsonResponse

# Create your views here.
def index(request):

    featured = Product.objects.filter(is_featured=True)
    newarrivals = Product.objects.order_by('-created_date')[:9]

    category = Category.objects.order_by('name')
    sub_category = Subcategory.objects.order_by('name')

    context = {
        'category':category,
        'sub_category':sub_category,
        'featured':featured,
        'newarrivals':newarrivals
    }

    return render(request, 'user/index.html', context)


def search(request):
    if request.method == 'POST':
        res = None

        keyword = request.POST.get('keyword')
        products = Product.objects.filter(name__icontains=keyword).order_by('name')

        if len(products) > 0 and len(keyword) > 0:
            data = []
            j = 0
            for i in products:
                item = {
                    'id':i.id,
                    'name':i.name,
                    'image':str(i.image1.url)
                }
                data.append(item)
                j+=1
                if j == 4:
                    break
            res = data
        else:
            res = 'No Products Found'


        return JsonResponse({'data':res})
    return JsonResponse({})
