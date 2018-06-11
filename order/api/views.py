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

from order.models import (
    Order
)

from .serializers import (
    OrderSerializer,
)

class PlaceOrderAPIView(CreateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CancelOrderAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
     
    def get(self, request, *args, **kwargs):
        try:
            order_obj = Order.objects.get(
                id=self.kwargs["order_id"]
            )
            if not (self.request.user == order_obj.user):
                message = {
                    "message": "You are not authorised to access this order"
                }
                return Response(message, status=HTTP_401_UNAUTHORIZED)
            order_obj.status = "Cancelled"
            order_obj.save()
            message = {
                "message": "success"
            }
            return Response(message, status=HTTP_200_OK)
        except Order.DoesNotExist:
            message = {
                "message": "Order Not Found"
            }
            return Response(message, status=HTTP_404_NOT_FOUND)


# class DispatchOrderAPIView(APIView):
#     authentication_classes = [JSONWebTokenAuthentication]
     
#     def get(self, request, *args, **kwargs):
#         try:
#             order_obj = Order.objects.get(
#                 id=self.kwargs["order_id"]
#             )
#             if not (self.request.user == order_obj.user):
#                 message = {
#                     "message": "You are not authorised to access this order"
#                 }
#                 return Response(message, status=HTTP_401_UNAUTHORIZED)
#             order_obj.status = "Cancelled"
#             order_obj.save()
#             message = {
#                 "message": "success"
#             }
#             return Response(message, status=HTTP_200_OK)
#         except Order.DoesNotExist:
#             message = {
#                 "message": "Order Not Found"
#             }
#             return Response(message, status=HTTP_404_NOT_FOUND)