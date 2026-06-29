from django.shortcuts import render
from products.models import product
def homemain(request):
    latest_products = product.objects.all().order_by('-id')[:3]
    context = {
        'products': latest_products
    }
    return render(request, 'index.html', context)
