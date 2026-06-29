from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import product, CartItem, Order, OrderItem

# Create your views here.

def allproducts_view(request):
      query = request.GET.get('q', '').strip()
      if query:
            allproductsname = product.objects.filter(name__icontains=query)
            allproductscatagory = product.objects.filter(catagory__icontains=query)
            allproducts = allproductsname.union(allproductscatagory)
      else:
            allproducts = product.objects.all()
      return render(request, 'products.html', {
            'allproducts': allproducts,
            'search_query': query,
      })

def products_by_category(request, category):
      category = category.lower()
      allproducts = product.objects.filter(catagory=category)
      category_display = dict(product.catagory_choices).get(category, category)
      return render(request, 'products.html', {
            'allproducts': allproducts,
            'category_name': category_display,
      })

@login_required
def add_to_cart(request, product_id):
      if request.method != 'POST':
            return redirect('products:allproducts')

      product_obj = get_object_or_404(product, pk=product_id)

      if product_obj.stock <= 0:
            messages.error(request, f"{product_obj.name} is out of stock.")
            return redirect('products:allproducts')

      cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product_obj,
            defaults={'quantity': 1}
      )

      if not created:
            if cart_item.quantity + 1 > product_obj.stock:
                  messages.error(request, f"Only {product_obj.stock} item(s) available for {product_obj.name}.")
                  return redirect('products:cart')
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

@login_required
def buy_now(request, product_id):
      if request.method != 'POST':
            return redirect('products:allproducts')

      product_obj = get_object_or_404(product, pk=product_id)
      quantity = int(request.POST.get('quantity', 1))
      
      if quantity <= 0:
            quantity = 1

      if product_obj.stock <= 0:
            messages.error(request, f"{product_obj.name} is out of stock.")
            return redirect('products:allproducts')

      if quantity > product_obj.stock:
            messages.error(request, f"Only {product_obj.stock} item(s) available for {product_obj.name}.")
            return redirect('products:allproducts')

      total_cost = product_obj.prices * quantity

      with transaction.atomic():
            product_obj.stock -= quantity
            product_obj.save()

            order = Order.objects.create(
                  user=request.user,
                  total_cost=total_cost,
            )
            
            OrderItem.objects.create(
                  order=order,
                  product=product_obj,
                  quantity=quantity,
                  price=product_obj.prices
            )

      messages.success(request, f"Order placed for {quantity} x {product_obj.name}.")
      return redirect('products:order_confirmation', order_id=order.id)

@login_required
def order_confirmation(request, order_id):
      order = get_object_or_404(Order, id=order_id, user=request.user)
      return render(request, 'order_confirmation.html', {'order': order})

@login_required
def order_history(request):
      orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
      return render(request, 'order_history.html', {'orders': orders})
