from django.contrib import admin
from .models import product
from .models import Order
from .models import CartItem
# Register your models here.

admin.site.register(product)
admin.site.register(Order)
admin.site.register(CartItem)