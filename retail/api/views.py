from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import random


from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_400_BAD_REQUEST, 
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.api.utils import generateToken, decodeToken
User = get_user_model()

from retail.models import (
    Retail_Info,
    Retail_Warehouse,
    Retail_Product,
)

from .serializers import (
    RegisterRetailSerializer,
    RetailerWarehouseSerializer,
    RegisterRetailDetailsSerializer,
    RetailProductSerializer,
)


from .permissions import (
    ProductPermission,
    RetailerPermission,
    WarehousePermission,
)

class RegisterRetailerAPIView(CreateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Retail_Info.objects.all()
    serializer_class = RegisterRetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DisplayRetailerAPIView(ListAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = RegisterRetailDetailsSerializer
    
    def get_queryset(self):
        retail_list = Retail_Info.objects.filter(
            user=self.request.user,
            status=True
        )
        return retail_list


class CloseRetailerAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            retail_obj = Retail_Info.objects.get(
                id=self.kwargs['id']
            )
            if not (retail_obj.user == self.request.user):
                message = {
                    "message": "You are not authorised to access this Retailer's data"
                }
                return Response(message, status=HTTP_401_UNAUTHORIZED)
            retail_obj.status = False
            retail_obj.save()
            message = {
                "message": "success"
            }
            return Response(message, status=HTTP_200_OK)
        except Retail_Info.DoesNotExist:
            message = {
                "message": "Retailer does not exist"
            }
            return Response(message, status=HTTP_404_NOT_FOUND)

    
class ReopenRetailerAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [RetailerPermission]

    def get(self, request, *args, **kwargs):
        try:
            retail_obj = Retail_Info.objects.get(
                id=self.kwargs['id']
            )
            if not (retail_obj.user == self.request.user):
                message = {
                    "message": "You are not authorised to access this Retailer's data"
                }
                return Response(message, status=HTTP_401_UNAUTHORIZED)
            retail_obj.status = True
            retail_obj.save()
            message = {
                "message": "success"
            }
            return Response(message, status=HTTP_200_OK)
        except Retail_Info.DoesNotExist:
            message = {
                "message": "Retailer does not exist"
            }
            return Response(message, status=HTTP_404_NOT_FOUND)


# Warehouse
class AddWarehouseAPIView(CreateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Retail_Warehouse.objects.all()
    serializer_class = RetailerWarehouseSerializer


class ListWarehouseAPIView(ListAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = RetailerWarehouseSerializer
    
    def get_queryset(self):
        warehouse_list = Retail_Warehouse.objects.filter(
            shop_name=self.kwargs["id"],
            status=True
        )
        return warehouse_list


class CloseWarehouseAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            warehouse_obj = Retail_Warehouse.objects.get(
                id=self.kwargs['id']
            )
            if not (warehouse_obj.shop_name.user == self.request.user):
                message = {
                    "message": "You are not authorised to access this Warehouse's data"
                }
                return Response(message, status=HTTP_401_UNAUTHORIZED)
            warehouse_obj.status = False
            warehouse_obj.save()
            message = {
                "message": "success"
            }
            return Response(message, status=HTTP_200_OK)
        except Retail_Warehouse.DoesNotExist:
            message = {
                "message": "Retailer does not exist"
            }
            return Response(message, status=HTTP_404_NOT_FOUND)


# Product
class AddProductAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        data = request.data
        warehouse_id = data.get("warehouse_id", None)
        product_title = data.get("product_title", None)
        quantity = data.get("quantity", None)
        domain = data.get("domain", None)
        category = data.get("category", None)
        delivery_time = data.get("delivery_time", None) 
        extra_data = data.get("extra_data", None)

        if(not warehouse_id or not product_title or not domain
            or not category or not delivery_time):
            message = {
                "message": "Please provide all the required fields"
            }
            return Response(message, status=HTTP_400_BAD_REQUEST)
        
        try:
            warehouse_obj = Retail_Warehouse.objects.get(
                id=warehouse_id
            )
            if not (warehouse_obj.shop_name.user == request.user):
                message = {
                    "message": "You are not authorised to access this retailer"
                }
                return Response(message, status=HTTP_401_UNAUTHORIZED)
            product_validate = Retail_Product.objects.filter(
                warehouse=warehouse_obj,
                product_title=product_title
            )
            if product_validate.exists():
                message = {
                    "message": "You already have a product of this name"
                }
                return Response(message, status=HTTP_400_BAD_REQUEST)
            Retail_Product.objects.create(
                warehouse=warehouse_obj,
                product_title=product_title,
                quantity=quantity,
                domain=domain,
                category=category,
                extra_data=extra_data,
                delivery_time=delivery_time
            )
            message = {
                "message": "success"
            }
            return Response(message, status=HTTP_200_OK)
        except Retail_Warehouse.DoesNotExist:
            message = {
                "message": "Please check the warehouse field"
            }
            return Response(message, status=HTTP_400_BAD_REQUEST)


class DisplayProductAPIView(RetrieveUpdateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = RetailProductSerializer
    permission_classes = [ProductPermission]
    lookup_field = 'id'
    queryset = Retail_Product.objects.all()



class AddQuantityAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [ProductPermission]

    def post(self, request, *args, **kwargs):
        data = request.data
        product_id = data.get("product_id", None)
        quantity = data.get("quantity", None)

        if(not product_id or not quantity):
            message = {
                "message": "Please provide all the required fields"
            }
            return Response(message, status=HTTP_400_BAD_REQUEST)
        
        try:
            product_obj = Retail_Product.objects.get(
                id=product_id
            )
            if not (product_obj.warehouse.shop_name.user == request.user):
                message = {
                    "message": "You are not authorised to access this retailer"
                }
                return Response(message, status=HTTP_401_UNAUTHORIZED)
            product_obj.quantity = product_obj.quantity + quantity
            product_obj.save()
            message = {
                "message": "success"
            }
            return Response(message, status=HTTP_200_OK)
        except Retail_Product.DoesNotExist:
            message = {
                "message": "No product found"
            }
            return Response(message, status=HTTP_404_NOT_FOUND)


class ProductListAPIView(ListAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = RetailProductSerializer
    
    def get_queryset(self):
        product_list = Retail_Product.objects.filter(
            status=True
        )
        return product_list


class DeleteProductAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [ProductPermission]

    def get(self, request, *args, **kwargs):
        try:
            product_obj = Retail_Product.objects.get(
                id=self.kwargs['id']
            )
            if not (self.request.user == product_obj.warehouse.shop_name.user):
                message = {
                    "message": "You are not authorised to access this product"
                }
                return Response(message, status=HTTP_401_UNAUTHORIZED)
            product_obj.status = False
            product_obj.save()
            message = {
                "message": "success"
            }
            return Response(message, status=HTTP_200_OK)
        except Retail_Product.DoesNotExist:
            message = {
                "message": "No Product Found"
            }
            return Response(message, status=HTTP_404_NOT_FOUND)