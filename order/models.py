from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

User = get_user_model()

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_list = JSONField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    total_cost = models.IntegerField(null=False)
    status = models.CharField(max_length=50, default="Order Placed")

    def __str__(self):
        return self.user.username