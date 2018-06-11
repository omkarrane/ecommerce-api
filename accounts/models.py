from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class User_Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, null=False)
    user_type = models.CharField(max_length=20, default='Customer')
    premium = models.BooleanField(default=False)
        
    def __str__(self):
        return self.user.username

class User_Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=200, null=False)
    pincode = models.CharField(max_length=6, null=False)

    def __str__(self):
        return self.user.username