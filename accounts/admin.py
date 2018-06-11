from django.contrib import admin
from .models import (
    User_Info,
    User_Address,
)

# Register your models here.
admin.site.register(User_Info)
admin.site.register(User_Address)
