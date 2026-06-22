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

