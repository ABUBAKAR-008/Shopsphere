from django.shortcuts import render
from .models import product
# Create your views here.

def allproducts_view(request):
      allproducts = product.objects.all()
      return render(request, 'products.html', {'allproducts' : allproducts})