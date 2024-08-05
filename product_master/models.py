from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    Category = models.CharField(max_length=50,verbose_name='Category Name')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')

    def __str__(self):
        return self.Category
    class Meta:
        db_table = 'category'

class ProductMaster(models.Model):
    name = models.CharField(max_length=50,verbose_name='Product Name')
    quantity = models.IntegerField(verbose_name='Quantity Available')
    desc = models.TextField(max_length=200,verbose_name='Description')
    price = models.FloatField(default=0.0,verbose_name='Price')
    published_date = models.DateField(default=None, null=True, verbose_name='Published Date')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Category')

    class Meta:
        db_table = 'product_master'

    def __str__(self):
        return self.name        

class CustomerOrders(models.Model):
    id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Customer') 
    order_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    product = models.ForeignKey(ProductMaster, on_delete=models.CASCADE, related_name='orders', verbose_name='Product')  


    class Meta:
        db_table = 'customer_orders'