from django.conf import settings
from django.db import models

# Create your models here.
class product(models.Model):
      catagory_choices=[
           ('sport', 'sports'),
           ('cloth', 'cloth'),
           ('fashion','fashion'),
           ('laptop','laptop'),
           ('pc','Computer'),
      ]
      name = models.CharField(max_length=240)
      photo = models.ImageField(upload_to='photos/', blank=True, null=True)
      description = models.TextField(max_length=300)
      catagory = models.CharField(choices=catagory_choices)
      stock = models.IntegerField()
      prices = models.IntegerField(default=0)

      def __str__(self):
          return self.name


class CartItem(models.Model):
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
      product = models.ForeignKey(product, on_delete=models.CASCADE)
      quantity = models.PositiveIntegerField(default=1)
      added_at = models.DateTimeField(auto_now_add=True)
      class Meta:
          unique_together = ('user', 'product')

      def __str__(self):
          return f"{self.quantity} x {self.product.name} for {self.user.username}"


class Order(models.Model):
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
      total_cost = models.IntegerField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

      def __str__(self):
            return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
      order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
      product = models.ForeignKey(product, on_delete=models.CASCADE)
      quantity = models.PositiveIntegerField()
      price = models.IntegerField()

      def __str__(self):
            return f"{self.quantity} x {self.product.name}"

