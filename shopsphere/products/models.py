from django.db import models
# Create your models here.
class product(models.Model):
      catagory_choices=[
           ('sp', 'sports'),
           ('clo', 'cloth'),
           ('fash','fashion'),
           ('lapt','laptop'),
           ('pc','Computer'),
      ]
      name = models.CharField(max_length=240)
      photo = models.ImageField(upload_to='photos/', blank=True, null=True)
      description = models.TextField(max_length=300)
      catagory = models.CharField(choices=catagory_choices)
      stock = models.IntegerField()

      
      def __str__(self):
          return self.name

