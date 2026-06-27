from django.shortcuts import render
from products.models import product
def homemain(request):
    latest_products = product.objects.all().order_by('-id')[:3]
    context = {
        'products': latest_products
    }
    return render(request, 'index.html', context)
def sports_catagory(request):
    sports_catagorys = product.objects.filter(catagory = "sport")
    context = {
        'sports' : sports_catagorys
    }

    return render(request, 'sports.html',context)

