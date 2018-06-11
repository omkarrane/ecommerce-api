from django.contrib import admin
from .models import (
    Retail_Info,
    Retail_Warehouse,
    Retail_Product
)

# Register your models here.
admin.site.register(Retail_Info)
admin.site.register(Retail_Warehouse)
admin.site.register(Retail_Product)