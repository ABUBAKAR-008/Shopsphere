from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import product, CartItem

# Create your views here.

def allproducts_view(request):
      allproducts = product.objects.all()
      return render(request, 'products.html', {'allproducts' : allproducts})

@login_required
def add_to_cart(request, product_id):
      if request.method != 'POST':
            return redirect('products:allproducts')

      product_obj = get_object_or_404(product, pk=product_id)
      cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product_obj,
            defaults={'quantity': 1}
      )

      if not created:
            cart_item.quantity += 1
            cart_item.save()  
      return redirect('products:cart')

@login_required
def cart_view(request):
      cart_items = CartItem.objects.filter(user=request.user).select_related('product')
      total_cost = 0
      for item in cart_items:
            item.subtotal = item.product.prices * item.quantity
            total_cost += item.subtotal

      return render(request, 'cart.html', {
            'cart_items': cart_items,
            'total_cost': total_cost,
      })
