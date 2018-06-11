from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
User = get_user_model()

# Create your models here.
class Retail_Info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200, unique=True, null=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.shop_name

class Retail_Warehouse(models.Model):
    shop_name = models.ForeignKey(Retail_Info, on_delete=models.CASCADE)
    city = models.CharField(max_length=20, null=False)
    state = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=200, null=False)
    pincode = models.CharField(max_length=7, null=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.shop_name.shop_name

class Retail_Product(models.Model):
    warehouse = models.ForeignKey(Retail_Warehouse, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=100, null=False)
    quantity = models.IntegerField(default=0, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    domain = models.CharField(max_length=20, null=False)
    category = models.CharField(max_length=20, null=False)
    delivery_time = models.CharField(max_length=40, null=False)
    extra_data = JSONField(null=True)
    status = models.BooleanField(default=True) # Display or Hide

    class Meta:
        unique_together = ('warehouse', 'product_title')

    def __str__(self):
        return self.product_title