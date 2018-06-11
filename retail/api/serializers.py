from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from accounts.api.utils import generateToken, decodeToken


import random

from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    PrimaryKeyRelatedField
)

from retail.models import (
    Retail_Info,
    Retail_Warehouse,
    Retail_Product
)

User = get_user_model()

# For Insert, Update Query
class RegisterRetailSerializer(ModelSerializer):

    class Meta:
        model = Retail_Info
        fields = [
            'shop_name'
        ]

# For Display Query
class RegisterRetailDetailsSerializer(ModelSerializer):

    class Meta:
        model = Retail_Info
        fields = [
            'id',
            'shop_name',
            'status',
            'rating'
        ]

class RetailerWarehouseSerializer(ModelSerializer):

    class Meta:
        model = Retail_Warehouse
        fields = '__all__'


class RetailProductSerializer(ModelSerializer):

    class Meta:
        model = Retail_Product
        fields = '__all__'
        read_only_fields = [
            'id',
            'warehouse'
        ]