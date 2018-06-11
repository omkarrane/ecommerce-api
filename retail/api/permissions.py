from rest_framework import permissions
from retail.models import (
    Retail_Info,
    Retail_Product,
    Retail_Warehouse
)


class RetailerPermission(permissions.BasePermission):
    message = "You are not authorised to access this Retailer's data"

    def has_object_permission(self, request, view, obj):
        return not (obj.user == request.user)


class WarehousePermission(permissions.BasePermission):
    message = "You are not authorised to access this Warehouse's data"

    def has_object_permission(self, request, view, obj):
        return (obj.shop_name.user == request.user)


class ProductPermission(permissions.BasePermission):
    message = "You are not authorised to access this Product's data"

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return (obj.warehouse.shop_name.user == request.user)