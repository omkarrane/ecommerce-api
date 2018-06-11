from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
import random


from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
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

from .utils import generateToken, decodeToken
User = get_user_model()

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserInfoSerializer,
    UserInfoDetailSerializer,
    UserAddressSerializer,
)

from accounts.models import (
    User_Info,
    User_Address,
)

from accounts.api.permissions import (
    OwnerPermission,
)

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.error, status=HTTP_400_BAD_REQUEST)


class SecuredAPIView(APIView):

    def get(self, request, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION']
        print(token)
        user_obj = decodeToken(token)
        if(not user_obj):
            message = {
                "message": "Please login again"
            }
            return Response(message, status=HTTP_400_BAD_REQUEST)
        return Response(user_obj)


class CreateUserInfoAPIView(CreateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = User_Info.objects.all()
    serializer_class = UserInfoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # user = User.objects.filter(
        #     username=request.user
        # )
        # user_info = User_Info.objects.filter(
        #     user=user[0]
        # )
        # print(user_info)
        # if user_info.exists():
        #     message = {
        #         "message": "Only one entry per user"
        #     }
        #     return Response(message, status=HTTP_400_BAD_REQUEST)
        return User_Info.objects.all()


class DisplayUserInfoAPIView(RetrieveAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = UserInfoDetailSerializer
    
    def get_object(self):
        user_info_obj = User_Info.objects.get(
            user=self.request.user
        )
        return user_info_obj

    
class UpdateUserInfoAPIView(RetrieveUpdateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = UserInfoSerializer
    
    def get_object(self):
        user_info_obj = User_Info.objects.get(
            user=self.request.user
        )
        return user_info_obj



# Address
class AddUserAddressAPIView(CreateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = User_Address.objects.all()
    serializer_class = UserAddressSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DisplayUserAddressAPIView(ListAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = UserAddressSerializer
    
    def get_queryset(self):
        user_address_list = User_Address.objects.filter(
            user=self.request.user
        )
        return user_address_list


class UpdateUserAddressAPIView(RetrieveUpdateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = UserAddressSerializer
    lookup_field = 'id'
    permission_classes = [OwnerPermission]
    queryset = User_Address.objects.all()


class DeleteUserAddressAPIView(DestroyAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = User_Address.objects.all()
    permission_classes = [OwnerPermission]
    serializer_class = UserAddressSerializer
    lookup_field = 'id'