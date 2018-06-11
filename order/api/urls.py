from django.conf.urls import url
from django.contrib import admin


from .views import (
    PlaceOrderAPIView,  
    CancelOrderAPIView, 
    # DispatchOrderAPIView,
)

app_name = 'order'


urlpatterns = [
    # Place Order API
    url(r'^place/order$', PlaceOrderAPIView.as_view(), name='place-order'),
    url(r'^cancel/order/(?P<order_id>\d+)$', CancelOrderAPIView.as_view(), name='cancel-order'),
    # url(r'^dispatch/order/(?P<order_id>\d+)$', DispatchOrderAPIView.as_view(), name='dispatch-order'),    
]