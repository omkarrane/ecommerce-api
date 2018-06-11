from django.conf.urls import url
from django.contrib import admin


from .views import (
    # Retailer
    RegisterRetailerAPIView,
    DisplayRetailerAPIView,
    CloseRetailerAPIView,
    ReopenRetailerAPIView,

    # Warehouse
    AddWarehouseAPIView,
    ListWarehouseAPIView,
    CloseWarehouseAPIView,

    # Product
    AddProductAPIView,
    DeleteProductAPIView,
    DisplayProductAPIView,
    AddQuantityAPIView,
    ProductListAPIView,
)

app_name = 'retail'


urlpatterns = [
    # Retail APIs
    url(r'^register/retailer$', RegisterRetailerAPIView.as_view(), name='register-retailer'),
    url(r'^detail/retailer$', DisplayRetailerAPIView.as_view(), name='display-retailer-details'),
    url(r'^close/retailer/(?P<id>\d+)$', CloseRetailerAPIView.as_view(), name='close-retailer'),
    url(r'^reopen/retailer/(?P<id>\d+)$', ReopenRetailerAPIView.as_view(), name='reopen-retailer'),
    
    # Warehouse APIs
    url(r'^add/warehouse$', AddWarehouseAPIView.as_view(), name='add-warehouse'),

        # Send Retailer ID
    url(r'^list/warehouse/(?P<id>\d+)$', ListWarehouseAPIView.as_view(), name='list-warehouse'),

        # Send Warehouse ID
    url(r'^close/warehouse/(?P<id>\d+)$', CloseWarehouseAPIView.as_view(), name='close-warehouse'),

    # Product APIs
    url(r'^add/product$', AddProductAPIView.as_view(), name='add-product'),
    url(r'^delete/product/(?P<id>\d+)$', DeleteProductAPIView.as_view(), name='delete-product'),    
    url(r'^detail/product/(?P<id>\d+)$', DisplayProductAPIView.as_view(), name='display-product-details'),    
    url(r'^update/product/(?P<id>\d+)$', DisplayProductAPIView.as_view(), name='update-product-details'),    
    url(r'^add/quantity/product$', AddQuantityAPIView.as_view(), name='add-quantity'),

    url(r'^list/all/products$', ProductListAPIView.as_view(), name='list-products'),        
]